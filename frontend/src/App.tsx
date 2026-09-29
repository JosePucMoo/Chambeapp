import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthLayout from "./pages/layout/AuthLayout";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";
import ForgotPassword from "./pages/auth/ForgotPassword";
import VerifyAccount from "./pages/auth/VerifyAccount";
import ResetPassword from "./pages/auth/ResetPassword";
import { Toaster } from "./components/ui/toast";
import { AuthProvider } from "./context/AuthProvider";
import { ProtectedRoute } from "./pages/layout/ProtectedRoute";
import MainLayout from "./pages/layout/MainLayout";
import MyTasks from "./pages/tasks/MyTasks";
import Dashboard from "./pages/dashboard/Dashboard";
import ProjectBoard from "./pages/projects/ProjectBoard";
import ProjectsList from "./pages/projects/ProjectsList";
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/auth" element={<AuthLayout />}>
            <Route index path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="forgot-password" element={<ForgotPassword />} />
            <Route path="reset-password/:token" element={<ResetPassword />} />
            <Route path="verify-account/:token" element={<VerifyAccount />} />
          </Route>
          <Route path="/" element={<ProtectedRoute />}>
            <Route element={<MainLayout />}>
              <Route index element={<Dashboard />} />

              <Route path="tasks" element={<MyTasks />} />

              <Route path="projects" element={<ProjectsList />} />
              <Route path="projects/:projectId" element={<ProjectBoard />} />
            </Route>
          </Route>
        </Routes>
        <Toaster />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
