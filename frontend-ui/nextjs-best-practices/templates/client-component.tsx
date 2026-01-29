'use client';

import { useState } from 'react';

interface Props {
  initialData?: any;
}

export function ClientComponent({ initialData }: Props) {
  const [state, setState] = useState(initialData);

  const handleAction = () => {
    // Interaction logic
    console.log('Action triggered');
  };

  return (
    <div className="flex flex-col gap-2">
      <p>Interactive State: {JSON.stringify(state)}</p>
      <button 
        onClick={handleAction}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
      >
        Click Me
      </button>
    </div>
  );
}
