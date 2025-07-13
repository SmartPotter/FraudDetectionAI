import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Upload from './pages/Upload';
import FraudDetection from './pages/FraudDetection';
import Blocklist from './pages/Blocklist';
import Dashboard from './pages/Dashboard';
import BlockchainLog from './pages/BlockchainLog';
import Report from './pages/Report';
import ReceiptVerification from './pages/ReceiptVerification';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/fraud-detection" element={<FraudDetection />} />
          <Route path="/blocklist" element={<Blocklist />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/blockchain-log" element={<BlockchainLog />} />
          <Route path="/report" element={<Report />} />
          <Route path="/receipt-verification" element={<ReceiptVerification />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;