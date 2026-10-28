import { lazy } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthLayout from "./pages/layout/AuthLayout";
import { Toaster } from "./components/ui/toast";
import { AuthProvider } from "./context/AuthProvider";
import { ProtectedRoute } from "./pages/layout/ProtectedRoute";
import MainLayout from "./pages/layout/MainLayout";

const Login = lazy(() => import("./pages/auth/Login"));
const Register = lazy(() => import("./pages/auth/Register"));
const ForgotPassword = lazy(() => import("./pages/auth/ForgotPassword"));
const VerifyAccount = lazy(() => import("./pages/auth/VerifyAccount"));
const ResetPassword = lazy(() => import("./pages/auth/ResetPassword"));
const AcceptInvitation = lazy(
  () => import("./pages/invitations/AcceptInvitation"),
);
const MyTasks = lazy(() => import("./pages/tasks/MyTasks"));
const CalendarPage = lazy(() => import("./pages/calendar/CalendarPage"));
const Dashboard = lazy(() => import("./pages/dashboard/Dashboard"));
const ProjectBoard = lazy(() => import("./pages/projects/ProjectBoard"));
const ProjectsList = lazy(() => import("./pages/projects/ProjectsList"));

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
          <Route element={<AuthLayout />}>
            <Route path="invitations/:token" element={<AcceptInvitation />} />
          </Route>
          <Route path="/" element={<ProtectedRoute />}>
            <Route element={<MainLayout />}>
              <Route index element={<Dashboard />} />

              <Route path="tasks" element={<MyTasks />} />

              <Route path="calendar" element={<CalendarPage />} />

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
