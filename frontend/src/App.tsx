import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import AppShell from './components/layout/AppShell';
import Dashboard from './pages/Dashboard';
import Knowledge from './pages/Knowledge';
import Courses from './pages/Courses';
import Assessment from './pages/Assessment';
import Planner from './pages/Planner';
import Assistant from './pages/Assistant';
import Progress from './pages/Progress';
import Settings from './pages/Settings';
import HelpSupport from './pages/HelpSupport';
import Profile from './pages/Profile';

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/knowledge" element={<Knowledge />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/assessment" element={<Assessment />} />
            <Route path="/planner" element={<Planner />} />
            <Route path="/assistant" element={<Assistant />} />
            <Route path="/progress" element={<Progress />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/help" element={<HelpSupport />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}
