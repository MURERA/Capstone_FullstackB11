import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Result from "./pages/Result";
import History from "./pages/History";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/result" element={<Result />} />
        <Route path="/history" element={<History />} />
        <Route path="/dashboard"element={<ProtectedRoute><Dashboard /></ProtectedRoute>}/>
        <Route path="/history"element={<ProtectedRoute><History /></ProtectedRoute>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
