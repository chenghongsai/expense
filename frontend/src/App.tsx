import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      {/* 后面再加其他页面；暂时默认重定向到 /login */}
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
