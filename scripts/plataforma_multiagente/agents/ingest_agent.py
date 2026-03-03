from google.adk.agents import Agent
from tools.supabase_tools import upload_file_to_supabase, save_dataset_metadata
from tools.data_tools import load_csv, load_excel

def get_ingest_agent():
    return Agent(
        name="IngestAgent",
        description="Carga archivos CSV o Excel, los guarda en Supabase y devuelve un DataFrame",
        tools=[
            upload_file_to_supabase,
            save_dataset_metadata,
            load_csv,
            load_excel
        ]
    )
