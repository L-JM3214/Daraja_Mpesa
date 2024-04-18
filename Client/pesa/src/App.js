import './App.css';
import Mpesa from './Components/Mpesa';
import { BrowserRouter as Router } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Mpesa />
      </div>
    </Router>
  );
}

export default App;