import { MantineProvider } from '@mantine/core';
import { useState } from 'react';
import './App.css';

import { Button } from '@mantine/core';
import { ClientContext, GraphQLClient, useMutation } from 'graphql-hooks';

const CREATE_SIMULATION_MUTATION = `mutation {
  createSimulation
}`

const client = new GraphQLClient({
  url: 'http://localhost:8080/graphql'
})

function Dashboard() {
  const [created, setCreated] = useState(false)
  const [createSimulation] = useMutation(CREATE_SIMULATION_MUTATION)
  return (
    <div className="App">
      <h1>Groundsim</h1>
      <Button onClick={async () => {
        const { data: { createSimulation: success } } = await createSimulation()
        setCreated(success)
      }}>
          created is {created ? "true" : "false"}
      </Button>
    </div>
  )
}

function App() {
  return (
    <MantineProvider withGlobalStyles withNormalizeCSS theme={{ colorScheme: 'dark' }}>
      <ClientContext.Provider value={client}>
        <Dashboard/>
      </ClientContext.Provider>
    </MantineProvider>
  )
}

export default App
