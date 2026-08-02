import { useState } from "react";

export type ToastType = "success" | "error" | "info";

export interface ToastItem {
  id: string;
  type: ToastType;
  title: string;
  message: string;
}

type Listener = (toasts: ToastItem[]) => void;
let toastListeners: Listener[] = [];
let toastQueue: ToastItem[] = [];

function notifyListeners() {
  toastListeners.forEach((listener) => listener([...toastQueue]));
}

export function showToast(title: string, message: string, type: ToastType = "info") {
  const id = Math.random().toString(36).substring(2, 9);
  const newToast: ToastItem = { id, type, title, message };
  toastQueue = [...toastQueue, newToast];
  notifyListeners();

  setTimeout(() => {
    toastQueue = toastQueue.filter((t) => t.id !== id);
    notifyListeners();
  }, 4500);
}

export function useToast() {
  const [toasts, setToasts] = useState<ToastItem[]>(toastQueue);

  useState(() => {
    const listener: Listener = (newToasts) => setToasts(newToasts);
    toastListeners.push(listener);
    return () => {
      toastListeners = toastListeners.filter((l) => l !== listener);
    };
  });

  const removeToast = (id: string) => {
    toastQueue = toastQueue.filter((t) => t.id !== id);
    notifyListeners();
  };

  return {
    toasts,
    toast: showToast,
    removeToast,
  };
}
