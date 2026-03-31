import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function getJson<T>(url: string): Promise<T> {
  const response = await api.get<T>(url);
  return response.data;
}

export async function postJson<T>(url: string, payload: unknown): Promise<T> {
  const response = await api.post<T>(url, payload);
  return response.data;
}