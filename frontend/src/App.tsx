import { useState } from 'react';
import './App.css';

import { Button } from '@mantine/core';

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <h1>Groundsim</h1>
      <Button onClick={() => setCount((count) => count + 1)}>
          count is {count}
      </Button>
    </div>
  )
}

export default App
