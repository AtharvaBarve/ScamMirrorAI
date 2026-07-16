import React from 'react';

const Input = React.forwardRef(({ className = '', ...props }, ref) => {
  return (
    <input
      ref={ref}
      className={`block w-full rounded-lg border border-border bg-surface/50 px-4 py-2.5 text-white placeholder:text-muted focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all duration-200 ${className}`}
      {...props}
    />
  );
});

Input.displayName = 'Input';

export default Input;
