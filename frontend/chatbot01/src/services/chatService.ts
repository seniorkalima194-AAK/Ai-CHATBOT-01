const apiBaseUrl = (
  // In development Vite forwards this path to the local backend. The same
  // relative URL also works behind the production Docker reverse proxy.
  import.meta.env.VITE_API_BASE_URL ?? "/api/v1"
).replace(/\/$/, "");

export type AnswerMode = "pdf_grounded" | "general_knowledge";

export interface ChatApiResponse {
  answer: string;
  answer_mode: AnswerMode;
  source_chunks: Array<{ source: string; page: number | null; score: number }>;
}

export interface TextbookUploadResult {
  source: string;
  status: "indexed" | "skipped" | "failed";
  chunks_indexed: number;
  message: string;
}

export interface DocumentStatus {
  chunks: number;
  sources: number;
  pdf_files: number;
  indexed_files: number;
}

export interface UploadedTextbook {
  filename: string;
  source: string;
  status: string;
  chunks_indexed: number;
}

interface TextbookUploadResponse {
  documents: TextbookUploadResult[];
}

interface UploadedTextbookResponse {
  documents: UploadedTextbook[];
}

export interface TextbookDeletionResult {
  source: string;
  chunks_removed: number;
  message: string;
}

async function errorMessage(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json();
    if (
      typeof body === "object" &&
      body !== null &&
      "detail" in body &&
      typeof body.detail === "string"
    ) {
      return body.detail;
    }
  } catch {
    // Fall back to a status message when the server did not send JSON.
  }
  return `Request failed (${response.status}).`;
}

export async function sendChatQuestion(question: string): Promise<ChatApiResponse> {
  const response = await fetch(`${apiBaseUrl}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  return response.json() as Promise<ChatApiResponse>;
}

export async function uploadTextbooks(files: File[]): Promise<TextbookUploadResult[]> {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  const response = await fetch(`${apiBaseUrl}/documents/upload`, {
    method: "POST",
    body: formData,
  });
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  const body = (await response.json()) as TextbookUploadResponse;
  return body.documents;
}

export async function getDocumentStatus(): Promise<DocumentStatus> {
  const response = await fetch(`${apiBaseUrl}/documents/status`);
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  return response.json() as Promise<DocumentStatus>;
}

export async function getUploadedTextbooks(): Promise<UploadedTextbook[]> {
  const response = await fetch(`${apiBaseUrl}/documents/uploads`);
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  const body = (await response.json()) as UploadedTextbookResponse;
  return body.documents;
}

export async function deleteUploadedTextbook(filename: string): Promise<TextbookDeletionResult> {
  const response = await fetch(
    `${apiBaseUrl}/documents/uploads/${encodeURIComponent(filename)}`,
    { method: "DELETE" },
  );
  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }
  return response.json() as Promise<TextbookDeletionResult>;
}
