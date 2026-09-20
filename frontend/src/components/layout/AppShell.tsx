import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function AppShell() {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex-1 lg:ml-[240px] flex flex-col min-h-screen">
        <Topbar />
        <main className="flex-1 p-5 lg:p-7" style={{ background: 'var(--color-page-bg)' }}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
