# Adding textbooks

No code changes are needed for each new book. The backend accepts normal,
text-based PDF files; PDFs made only from scanned page images need OCR first.

## Option 1: Add PDFs in Settings

Open **Settings**, choose **Upload book**, then select one or more `.pdf`
files. In the local installation, the backend copies each selected file into
`backend/Books/uploads/` on this same computer and indexes it immediately. The
book stays in the original location too. A file with the same name replaces the
older uploaded version of that book.

## Option 2: Add a large collection through the folder

Copy PDFs (including folders of PDFs) anywhere inside:

`backend/Books/`

Keep the backend running. It checks this folder every 60 seconds and indexes
only new or changed PDFs in the background, so students can keep asking
questions. A first import of about 100 textbooks can take considerable time on
CPU; leave the backend running until it finishes.

The progress endpoint is:

`GET /api/v1/documents/status`

The scan interval can be changed in `backend/.env` with
`DOCUMENT_SCAN_INTERVAL_SECONDS=60` (minimum: 10 seconds).

Each chat-uploaded PDF is limited to 100 MB. Folder imports have no application
size limit, although very large files take longer to read and index.
