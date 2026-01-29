import React, { createContext, useReducer, Dispatch } from 'react';

interface Item { id: string; name: string; }

interface State {
  items: Item[]
  selectedItem: Item | null
  loading: boolean
}

type Action =
  | { type: 'SET_ITEMS'; payload: Item[] }
  | { type: 'SELECT_ITEM'; payload: Item }
  | { type: 'SET_LOADING'; payload: boolean }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'SET_ITEMS':
      return { ...state, items: action.payload }
    case 'SELECT_ITEM':
      return { ...state, selectedItem: action.payload }
    case 'SET_LOADING':
      return { ...state, loading: action.payload }
    default:
      return state
  }
}

const AppContext = createContext<{
  state: State
  dispatch: Dispatch<Action>
} | undefined>(undefined)

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(reducer, {
    items: [],
    selectedItem: null,
    loading: false
  })

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  )
}
