import fitz  # PyMuPDF
import os
import zipfile
from concurrent.futures import ThreadPoolExecutor  # 并行处理，提升大批量效率

def extract_pdf_to_md(pdf_path, md_path):
    """单篇PDF转MD，适配大批量并行处理"""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()  # 提取全文文本
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text)
        doc.close()
        return f"Success: {os.path.basename(pdf_path)} → MD"
    except Exception as e:
        return f"Failed: {os.path.basename(pdf_path)}，错误：{str(e)}"

def unzip_papers(zip_path, extract_dir):
    """批量解压zip，支持多文件解压"""
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    return f"解压完成，共解压 {len(zip_ref.namelist())} 个文件"

def batch_process_pdfs(pdf_dir, output_md_dir, max_workers=5):
    """批量处理PDF，并行提取，提升效率（适配大批量）"""
    os.makedirs(output_md_dir, exist_ok=True)
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    results = []
    
    # 并行处理，最多5个线程（可调整，避免占用过多资源）
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for idx, pdf_file in enumerate(pdf_files, 1):
            # 加序号，避免大批量论文重名
            md_filename = f"{idx:02d}_{os.path.splitext(pdf_file)[0]}.md"
            pdf_path = os.path.join(pdf_dir, pdf_file)
            md_path = os.path.join(output_md_dir, md_filename)
            futures.append(executor.submit(extract_pdf_to_md, pdf_path, md_path))
        
        # 收集结果
        for future in futures:
            results.append(future.result())
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python pdf_extract.py <input_pdf_or_zip> <output_md_dir>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    temp_pdf_dir = "./papers-pdf-temp"
    os.makedirs(temp_pdf_dir, exist_ok=True)

    # 处理zip压缩包（大批量PDF）
    if input_path.endswith(".zip"):
        print(unzip_papers(input_path, temp_pdf_dir))
        # 批量并行处理解压后的PDF
        results = batch_process_pdfs(temp_pdf_dir, output_dir)
        for res in results:
            print(res)
    # 处理单个/多个PDF文件
    elif input_path.endswith(".pdf"):
        md_path = os.path.join(output_dir, f"01_{os.path.splitext(os.path.basename(input_path))[0]}.md")
        print(extract_pdf_to_md(input_path, md_path))
    else:
        print("Unsupported file type: 仅支持PDF和zip压缩包")