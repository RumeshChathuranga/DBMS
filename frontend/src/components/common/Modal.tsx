import React, { useEffect } from "react";
import { X } from "lucide-react";
import { createPortal } from "react-dom";

type ModalSize = "sm" | "md" | "lg" | "xl";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: ModalSize;
  children: React.ReactNode;
}

const sizeClasses: Record<ModalSize, string> = {
  sm: "max-w-sm",
  md: "max-w-lg",
  lg: "max-w-3xl",
  xl: "max-w-5xl",
};

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  size = "md",
  children,
}) => {
  // Lock body scroll while open
  useEffect(() => {
    if (!isOpen) return;
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = prev;
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-[1200]">
      {/* Overlay covers entire viewport */}
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
        aria-hidden="true"
      />
      {/* Modal container */}
      <div className="absolute inset-0 flex items-start md:items-center justify-center p-4 md:p-6">
        <div
          className={`w-full ${sizeClasses[size]} bg-white rounded-xl shadow-2xl`}
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-title"
          onClick={(e) => e.stopPropagation()}
        >
          {(title || onClose) && (
            <div className="flex items-center justify-between px-5 py-4 border-b">
              {title ? (
                <h2 id="modal-title" className="text-xl font-semibold">
                  {title}
                </h2>
              ) : (
                <span />
              )}
              <button
                type="button"
                aria-label="Close"
                onClick={onClose}
                className="p-2 rounded hover:bg-gray-100"
              >
                <X size={20} />
              </button>
            </div>
          )}

          <div className="p-5">{children}</div>
        </div>
      </div>
    </div>,
    document.body
  );
};

export default Modal;
