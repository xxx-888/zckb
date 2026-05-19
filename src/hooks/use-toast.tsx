import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'

export type ToastType = 'default' | 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: string
  title: string
  description?: string
  type: ToastType
  duration?: number
}

interface ToastContextType {
  toasts: Toast[]
  addToast: (toast: Omit<Toast, 'id'>) => void
  removeToast: (id: string) => void
}

const ToastContext = createContext<ToastContextType | undefined>(undefined)

export const ToastProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([])

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = Math.random().toString(36).substr(2, 9)
    const newToast: Toast = {
      ...toast,
      id,
      duration: toast.duration || 5000,
    }
    setToasts((prev) => [...prev, newToast])

    if (newToast.duration && newToast.duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, newToast.duration)
    }
  }, [removeToast])

  return (
    <ToastContext.Provider value={{ toasts, addToast, removeToast }}>
      {children}
    </ToastContext.Provider>
  )
}

export const useToast = () => {
  const context = useContext(ToastContext)
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }

  const success = useCallback((title: string, description?: string) => {
    context.addToast({ title, description, type: 'success' })
  }, [context])

  const error = useCallback((title: string, description?: string) => {
    context.addToast({ title, description, type: 'error', duration: 7000 })
  }, [context])

  const warning = useCallback((title: string, description?: string) => {
    context.addToast({ title, description, type: 'warning' })
  }, [context])

  const info = useCallback((title: string, description?: string) => {
    context.addToast({ title, description, type: 'info' })
  }, [context])

  return {
    toasts: context.toasts,
    removeToast: context.removeToast,
    success,
    error,
    warning,
    info,
  }
}

export default useToast
