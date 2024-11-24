import PyPDF2

# Open the PDF file
def userData():
    with open("Resume_Debasish_Research.pdf", "rb") as file:
        reader = PyPDF2.PdfReader(file)
        
        # Get number of pages
        num_pages = len(reader.pages)
        
        # Extract text from each page
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Safely print the text
            try:
                return(f"Page {page_num + 1} Text:\n{text}\n")
            except UnicodeEncodeError:
                return(f"Page {page_num + 1} Text (encoding error):\n{repr(text)}\n")

