import pandas as pd
import io

def generate_excel_report(df_eval: pd.DataFrame) -> bytes:
    """
    Menghasilkan file Excel biner dari DataFrame ranking untuk tombol download Streamlit.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_eval.to_excel(writer, sheet_name='Ranking Petugas', index=False)
        
        # Format tambahan (opsional untuk mempercantik sheet)
        workbook = writer.book
        worksheet = writer.sheets['Ranking Petugas']
        
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#00288e',
            'font_color': '#ffffff',
            'border': 1
        })
        
        for col_num, value in enumerate(df_eval.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
    processed_data = output.getvalue()
    return processed_data