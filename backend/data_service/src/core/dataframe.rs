use polars::prelude::*;
use serde::{Deserialize, Serialize};
use calamine::{open_workbook_auto, Reader, Data as CalamineData};
use std::fs::File;
use std::io::Write;

#[derive(Serialize, Deserialize, Debug)]
pub struct ColumnSchema {
    pub name: String,
    pub data_type: String,
    pub null_count: usize,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct DatasetSchema {
    pub dataset_id: String,
    pub row_count: usize,
    pub columns: Vec<ColumnSchema>,
}

pub fn convert_xlsx_to_csv(xlsx_path: &str, csv_path: &str) -> Result<(), String> {
    let mut excel = open_workbook_auto(xlsx_path).map_err(|e| e.to_string())?;
    
    let sheet_names = excel.sheet_names().to_vec();
    if sheet_names.is_empty() {
        return Err("No sheets found in XLSX file".to_string());
    }
    let first_sheet = &sheet_names[0];
    
    if let Ok(range) = excel.worksheet_range(first_sheet) {
        let mut file = File::create(csv_path).map_err(|e| e.to_string())?;
        
        for row in range.rows() {
            let cols: Vec<String> = row.iter().map(|c| {
                match c {
                    CalamineData::String(s) => format!("\"{}\"", s.replace("\"", "\"\"")),
                    CalamineData::Float(f) => f.to_string(),
                    CalamineData::Int(i) => i.to_string(),
                    CalamineData::Bool(b) => b.to_string(),
                    CalamineData::Empty => String::new(),
                    CalamineData::Error(e) => format!("\"{:?}\"", e),
                    _ => c.to_string(),
                }
            }).collect();
            writeln!(file, "{}", cols.join(",")).map_err(|e| e.to_string())?;
        }
        Ok(())
    } else {
        Err(format!("Could not read range for sheet: {}", first_sheet))
    }
}

pub fn extract_schema_from_csv(file_path: &str, dataset_id: &str) -> Result<DatasetSchema, PolarsError> {
    // We read eagerly here to get exact null counts and row count easily for the schema.
    let df = CsvReader::from_path(file_path)?
        .infer_schema(Some(100))
        .has_header(true)
        .finish()?;

    let row_count = df.height();
    let mut columns = Vec::new();

    for field in df.schema().iter_fields() {
        let name = field.name().to_string();
        let data_type = field.data_type().to_string();
        
        // Count nulls for this column
        let series = df.column(&name)?;
        let null_count = series.null_count();

        columns.push(ColumnSchema {
            name,
            data_type,
            null_count,
        });
    }

    Ok(DatasetSchema {
        dataset_id: dataset_id.to_string(),
        row_count,
        columns,
    })
}

pub fn clean_dataset(file_path: &str, output_path: &str) -> Result<usize, PolarsError> {
    let df = CsvReader::from_path(file_path)?
        .infer_schema(Some(100))
        .has_header(true)
        .finish()?;
    
    // Pour la Phase 2 : On supprime les doublons et les valeurs manquantes
    let mut cleaned_df = df.unique(None, UniqueKeepStrategy::First, None)?
        .drop_nulls::<String>(None)?;
        
    let new_row_count = cleaned_df.height();
    
    let mut file = std::fs::File::create(output_path)?;
    CsvWriter::new(&mut file)
        .finish(&mut cleaned_df)?;
        
    Ok(new_row_count)
}

pub fn get_dataset_preview_json(file_path: &str, limit: usize) -> Result<serde_json::Value, PolarsError> {
    let df = CsvReader::from_path(file_path)?
        .infer_schema(Some(100))
        .has_header(true)
        .finish()?;

    let rows_to_take = std::cmp::min(limit, df.height());
    let mut sub_df = df.slice(0, rows_to_take);

    let mut buf = Vec::new();
    JsonWriter::new(&mut buf)
        .with_json_format(JsonFormat::Json)
        .finish(&mut sub_df)?;

    let json_val: serde_json::Value = serde_json::from_slice(&buf).unwrap_or(serde_json::json!([]));
    Ok(json_val)
}

pub fn extract_columns_json(file_path: &str, columns: &[String]) -> Result<serde_json::Value, PolarsError> {
    let df = CsvReader::from_path(file_path)?
        .infer_schema(Some(100))
        .has_header(true)
        .finish()?;

    let valid_cols: Vec<&str> = columns
        .iter()
        .map(|s| s.as_str())
        .filter(|c| df.schema().contains(c))
        .collect();

    let mut sub_df = if valid_cols.is_empty() {
        df
    } else {
        df.select(valid_cols)?
    };

    let mut buf = Vec::new();
    JsonWriter::new(&mut buf)
        .with_json_format(JsonFormat::Json)
        .finish(&mut sub_df)?;

    let json_val: serde_json::Value = serde_json::from_slice(&buf).unwrap_or(serde_json::json!([]));
    Ok(json_val)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use std::io::Write;

    fn create_test_csv(path: &str) {
        let mut file = fs::File::create(path).unwrap();
        writeln!(file, "id,name,score").unwrap();
        writeln!(file, "1,Alice,85.5").unwrap();
        writeln!(file, "2,Bob,90.0").unwrap();
        writeln!(file, "3,,75.0").unwrap(); // missing name
        writeln!(file, "2,Bob,90.0").unwrap(); // duplicate
    }

    #[test]
    fn test_extract_schema() {
        let test_path = "./test_schema.csv";
        create_test_csv(test_path);

        let schema = extract_schema_from_csv(test_path, "test_id").unwrap();
        assert_eq!(schema.dataset_id, "test_id");
        assert_eq!(schema.row_count, 4);
        assert_eq!(schema.columns.len(), 3);
        
        let null_col = schema.columns.iter().find(|c| c.name == "name").unwrap();
        assert_eq!(null_col.null_count, 1);

        fs::remove_file(test_path).unwrap();
    }

    #[test]
    fn test_clean_dataset() {
        let test_path = "./test_clean.csv";
        let out_path = "./test_clean_out.csv";
        create_test_csv(test_path);

        let new_rows = clean_dataset(test_path, out_path).unwrap();
        // Original has 4 rows. 1 has missing name, 1 is duplicate.
        // After unique + drop nulls, should be 2 rows (Alice, Bob).
        assert_eq!(new_rows, 2);

        fs::remove_file(test_path).unwrap();
        fs::remove_file(out_path).unwrap();
    }
}
