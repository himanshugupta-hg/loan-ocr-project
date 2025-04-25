import streamlit as st
import tempfile
import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
from utils.preprocessing import preprocess_image
from utils.ocr_processor import extract_text, parse_loan_data
from utils.validation import validate_data
from utils.integration import send_to_bank_system

# Configure Tesseract path (update with your actual path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\KIIT\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Configure Poppler path (update with your actual path)
POPPLER_PATH = r'C:\Users\KIIT\poppler-24.08.0-0\Library\bin'

st.set_page_config(page_title="LoanDoc AI Processor", layout="wide")

def secure_temp_file(uploaded_file):
    """Handle temporary file creation with proper cleanup"""
    try:
        file_ext = os.path.splitext(uploaded_file.name)[1]
        temp_dir = tempfile.gettempdir()
        
        # Create temp file with unique name
        with tempfile.NamedTemporaryFile(
            dir=temp_dir,
            suffix=file_ext,
            delete=False
        ) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
            
        # Explicitly close file handle
        if hasattr(tmp_file, 'close'):
            tmp_file.close()
            
        return tmp_path
        
    except Exception as e:
        st.error(f"Temp file creation failed: {str(e)}")
        return None

def main():
    st.title("🏦 Automated Loan Document Processing")
    st.markdown("### Upload loan documents for automated processing")

    uploaded_file = st.file_uploader(
        "Drag and drop or click to upload PDF/Image", 
        type=['pdf', 'png', 'jpg', 'jpeg']
    )

    if uploaded_file:
        tmp_path = None
        try:
            # Step 1: Secure temp file creation
            tmp_path = secure_temp_file(uploaded_file)
            if not tmp_path or not os.path.exists(tmp_path):
                raise FileNotFoundError("Temporary file creation failed")

            # Step 2: Document processing
            with st.spinner("Analyzing document..."):
                processed_image = preprocess_image(tmp_path, poppler_path=POPPLER_PATH)
                
                if processed_image is None:
                    st.error("Document processing failed")
                    return

                # Step 3: OCR Processing
                text = extract_text(Image.fromarray(processed_image))
                data = parse_loan_data(text)

            # In the processing block after text extraction:
            st.subheader("🔍 Raw OCR Output")
            st.text_area("Full extracted text", text, height=300)

            # Add debug preview
            st.json({
                "OCR Statistics": {
                    "Characters": len(text),
                    "Lines": len(text.split('\n')),
                    "Words": len(text.split())
                }
            })

            # Display results
            st.success("Document processed successfully!")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📄 Extracted Data")
                edited_data = {}
                fields = ['name', 'address', 'income', 'loan_amount', 'ssn']
                
                for field in fields:
                    value = data.get(field, '')
                    edited = st.text_input(
                        label=field.replace('_', ' ').title(),
                        value=value,
                        key=f"edit_{field}"
                    )
                    edited_data[field] = edited

            with col2:
                st.subheader("🔍 Processing Details")
                st.metric("Text Length", f"{len(text)} characters")
                st.download_button(
                    label="Download Raw Text",
                    data=text,
                    file_name="ocr_output.txt"
                )

            # Validation and Submission
            if st.button("✅ Validate & Submit"):
                with st.spinner("Validating..."):
                    validation_errors = validate_data(edited_data)
                    
                    if validation_errors:
                        st.error("Validation Issues Found:")
                        for error in validation_errors:
                            st.write(f"• {error}")
                    else:
                        if send_to_bank_system(edited_data):
                            st.success("Data submitted successfully!")
                            st.balloons()
                        else:
                            st.error("Submission failed. Possible reasons:")
                            st.markdown("""
                            1. Connection to bank system unavailable
                            2. Invalid data formatting
                            3. Authentication issues
                            """)
                            st.markdown("Check logs for detailed error information.")

        except PermissionError as pe:
            st.error(f"Access denied: {str(pe)}\n\n"
                     "Please check:\n"
                     "1. Antivirus settings\n"
                     "2. File permissions\n"
                     "3. Temporary directory access")
        except Exception as e:
            st.error(f"Processing failed: {str(e)}")
            st.text("Debug Info:")
            st.json({
                "temp_file": tmp_path,
                "file_size": os.path.getsize(tmp_path) if tmp_path else 0,
                "exists": os.path.exists(tmp_path) if tmp_path else False
            })
        finally:
            # Cleanup resources
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception as cleanup_error:
                    st.warning(f"Cleanup failed: {str(cleanup_error)}")

if __name__ == "__main__":
    main()