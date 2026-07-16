import Routes from './routes';
import { AnalysisProvider } from './context/AnalysisContext';

function App() {
  return (
    <AnalysisProvider>
      <>
        <Routes />
      </>
    </AnalysisProvider>
  );
}

export default App;