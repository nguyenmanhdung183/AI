import os
import comtypes.client

def ppt_to_pdf(input_folder, output_folder):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    
    files = os.listdir(input_folder)
    ppt_files = [f for f in files if f.endswith(".ppt") or f.endswith(".pptx")]
    
    for ppt_file in ppt_files:
        input_path = os.path.join(input_folder, ppt_file)
        output_path = os.path.join(output_folder, os.path.splitext(ppt_file)[0] + ".pdf")
        
        print(f"Converting {input_path} to {output_path}...")
        
        deck = powerpoint.Presentations.Open(input_path)
        deck.SaveAs(output_path, 32)  # 32 is the PDF format
        deck.Close()
    
    powerpoint.Quit()
    
input_folder = r"C:\Users\NGUYEN MANH DUNG\Desktop\ppt2pdf\in"
output_folder = r"C:\Users\NGUYEN MANH DUNG\Desktop\ppt2pdf\out"


ppt_to_pdf(input_folder, output_folder)
