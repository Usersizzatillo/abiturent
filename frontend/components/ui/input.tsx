import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, id, ...props }, ref) => {
    const inputId = id ?? props.name;
    return (
      <div className="flex flex-col gap-1.5">
        {label ? (
          <label htmlFor={inputId} className="label">
            {label}
          </label>
        ) : null}
        <div className={cn(error && "relative")}>
          <input
            ref={ref}
            id={inputId}
            className={cn("input", error && "border-danger", className)}
            aria-invalid={!!error}
            {...props}
          />
        </div>
        {error ? (
          <p role="alert" className="text-sm text-danger">
            {error}
          </p>
        ) : hint ? (
          <p className="text-xs text-subtle">{hint}</p>
        ) : null}
      </div>
    );
  }
);
Input.displayName = "Input";

export { Input };