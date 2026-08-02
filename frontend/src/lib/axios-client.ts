import axios, { AxiosInstance, AxiosError } from "axios";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

/**
 * Pre-configured Axios Instance for Backend REST API communication.
 */
export const axiosClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15 seconds timeout
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

// Interceptor for standardized error handling
axiosClient.interceptors.response.use(
  (response: any) => response,
  (error: AxiosError) => {
    let errorMessage = "An unexpected error occurred while communicating with the server.";

    if (error.response) {
      // Backend returned error status code (4xx or 5xx)
      const data = error.response.data as any;
      errorMessage = data?.detail || data?.message || `HTTP Error ${error.response.status}`;
    } else if (error.request) {
      // Request was made but no response received (Network or CORS error)
      errorMessage = "Unable to connect to research backend server. Please verify the backend is running at http://localhost:8000.";
    } else {
      errorMessage = error.message || errorMessage;
    }

    return Promise.reject(new Error(errorMessage));
  }
);
