"""
Process an existing downloaded PDF through the IPO analysis pipeline
"""

import os
import sys
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
# Force UTF-8 output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from tools.drhp_extractor import extract_drhp_to_json
from agents.financial_agent import extract_financial_metrics
from agents.risk_agent import extract_risks
from agents.cerebras_report_generator_agent import generate_ipo_report, save_report
from config import SETTINGS


def process_pdf(pdf_path, company_name):
    """Process a single PDF through the complete pipeline."""
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Processing: {os.path.basename(pdf_path)}")
    print(f"Company: {company_name}")
    print("=" * 60)
    
    # Determine output paths
    safe_name = company_name.replace(" ", "_")
    output_dir = os.path.join("data", safe_name, "extracted")
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    extraction_output = os.path.join(output_dir, f"{base_name}.json")
    analysis_output = os.path.join(output_dir, f"{base_name}_analysis.json")
    report_output = os.path.join(output_dir, f"{base_name}_report.md")
    
    # Stage 3: Extract PDF to JSON
    print(f"\n📄 Stage 3 — Extracting PDF to JSON")
    try:
        extract_drhp_to_json(pdf_path, extraction_output)
        print(f"✅ Extraction complete: {extraction_output}")
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Stage 5: Analyze extracted data
    print(f"\n📊 Stage 5 — Financial & Risk Analysis")
    
    try:
        # Load extracted JSON
        with open(extraction_output, "r", encoding="utf-8") as f:
            extracted_data = json.load(f)
        
        # Run financial analysis
        print("   💰 Analyzing financial metrics...")
        financial_analysis = extract_financial_metrics(extracted_data)
        
        # Run risk analysis
        print("   ⚠️  Identifying risks...")
        risk_analysis = extract_risks(extracted_data)
        
        # Combine analyses
        analysis_results = {
            "source_file": os.path.basename(pdf_path),
            "company": company_name,
            "financial_analysis": financial_analysis,
            "risk_analysis": risk_analysis,
            "analysis_metadata": {
                "stage": "Stage 5 - Analysis",
                "methods": "Rule-based, deterministic",
                "inference": "None - explicit data only"
            }
        }
        
        # Save analysis results
        with open(analysis_output, "w", encoding="utf-8") as f:
            json.dump(analysis_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Analysis complete: {analysis_output}")
        print(f"   💰 Financial metrics found: {financial_analysis.get('metrics_found', 0)}")
        print(f"   ⚠️  Risks identified: {risk_analysis.get('risk_count', 0)}")
        
    except Exception as e:
        print(f"❌ Error analyzing PDF: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Stage 6: Generate IPO Report
    print(f"\n📝 Stage 6 — IPO Report Generation")
    
    try:
        report = generate_ipo_report(analysis_results, SETTINGS.CEREBRAS_API_KEY)
        save_report(report, report_output)
        
        print(f"✅ Report generated: {report_output}")
        
    except Exception as e:
        print(f"⚠️  Report generation skipped: {e}")
        print("   (Analysis JSON is still available)")
    
    print(f"\n{'=' * 60}")
    print("🎉 Pipeline completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    # Available PDFs
    pdfs = {
        "1": ("Aequs", r"data\Aequs\drhp\1765169850233.pdf"),
        "2": ("Nephrocare", r"data\Nephrocare\drhp\1764758442229.pdf"),
        "3": ("Orkla India Limited", r"data\Orkla_India_Limited\drhp\1763620246979.pdf"),
        "4": ("Meesho", r"data\meesho\drhp\1764314864285.pdf"),
    }
    
    print("\n📋 Available PDFs:")
    for key, (company, path) in pdfs.items():
        size = os.path.getsize(path) / (1024 * 1024) if os.path.exists(path) else 0
        status = "✅" if size > 1 else "⚠️"
        print(f"   {key}. {company:25s} - {size:6.2f} MB {status}")
    
    choice = input("\nSelect PDF to process (1-4): ").strip()
    
    if choice in pdfs:
        company, pdf_path = pdfs[choice]
        process_pdf(pdf_path, company)
    else:
        print("❌ Invalid choice")
