export interface ApiResponse<T = unknown> {
  ok: boolean;
  message: string;
  data: T;
}

export interface ErrorDetail {
  type: string;
  message: string;
  timestamp: string;
}

export interface ErrorResponse {
  detail: ErrorDetail[];
}
