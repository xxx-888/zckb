import { Routes, Route, Navigate } from 'react-router-dom';
import { ToastProvider, useToast } from './hooks/use-toast';
import Toaster from './components/ui/toaster';

// 管理员页面
import { AdminLogin } from './pages/admin/AdminLogin';
import { AdminGuard } from './components/AdminGuard';
import { AdminDashboard } from './pages/admin/AdminDashboard';
import { AIConfig } from './pages/admin/AIConfig';
import { CompetitorAnalysis } from './pages/admin/CompetitorAnalysis';
import { NotificationConfig } from './pages/admin/NotificationConfig';
import { PermissionManagement } from './pages/admin/PermissionManagement';
import { ReplyAudit } from './pages/admin/ReplyAudit';
import { ReviewManagement } from './pages/admin/ReviewManagement';
import { SpiderManagement } from './pages/admin/SpiderManagement';
import { StoreManagement } from './pages/admin/StoreManagement';
import { AnnualReport } from './pages/admin/AnnualReport';
import { XiaohongshuPage } from './pages/admin/XiaohongshuPage';
import { XiaohongshuAnalysis } from './pages/admin/XiaohongshuAnalysis';
import { NegativeReply as AdminNegativeReply } from './pages/admin/NegativeReply';
import { PositiveActivation as AdminPositiveActivation } from './pages/admin/PositiveActivation';
import { Insights as AdminInsights } from './pages/admin/Insights';
import { AIAnalysis as AdminAIAnalysis } from './pages/admin/AIAnalysis';
import { MobileSettings as AdminMobileSettings } from './pages/admin/MobileSettings';

// 管理员页面 - AI配置子页面
import { Evaluation } from './pages/admin/AIConfig/Evaluation';
import { ModelConfig } from './pages/admin/AIConfig/ModelConfig';
import { Monitoring } from './pages/admin/AIConfig/Monitoring';
import { PromptConfig } from './pages/admin/AIConfig/PromptConfig';
import { RuleEngine } from './pages/admin/AIConfig/RuleEngine';

// 移动端页面
import { Login } from './pages/mobile/Login';
import { Register } from './pages/mobile/Register';
import { ForgotPassword } from './pages/mobile/ForgotPassword';
import { Dashboard } from './pages/mobile/Dashboard';
import { StoreSettings } from './pages/mobile/StoreSettings';
import { ReplyTemplate } from './pages/mobile/ReplyTemplate';
import { PlatformConnection } from './pages/mobile/PlatformConnection';
import { NotificationSettings } from './pages/mobile/NotificationSettings';
import { AutoReplySettings } from './pages/mobile/AutoReplySettings';
import { HelpCenter } from './pages/mobile/HelpCenter';
import { Subscription } from './pages/mobile/Subscription';
import { DishElimination } from './pages/mobile/DishElimination';
import { StoreList } from './pages/mobile/StoreList';
import { StoreDetail } from './pages/mobile/StoreDetail';
import { AIAnalysis } from './pages/mobile/AIAnalysis';
import { Insights } from './pages/mobile/Insights';
import { NegativeReply } from './pages/mobile/NegativeReply';
import { PositiveActivation } from './pages/mobile/PositiveActivation';
import { ReviewStream } from './pages/mobile/ReviewStream';
import { ReviewDetail } from './pages/mobile/ReviewDetail';
import { Settings } from './pages/mobile/Settings';
import { PlatformDetail } from './pages/mobile/PlatformDetail';
import { MobileAnnualReport } from './pages/mobile/AnnualReport';
import { MobileCompetitorAnalysis } from './pages/mobile/CompetitorAnalysis';
import TraceabilityDetail from './pages/mobile/TraceabilityDetail';

// 应用内容组件 - 在 ToastProvider 内部使用 useToast
function AppContent() {
  const { toasts, removeToast } = useToast();

  return (
    <>
      <Routes>
        {/* 默认重定向 */}
        <Route path="/" element={<Navigate to="/mobile" replace />} />
        
        {/* ==================== 移动端路由 ==================== */}
        <Route path="/mobile" element={<Dashboard />} />
        <Route path="/mobile/login" element={<Login />} />
        <Route path="/mobile/register" element={<Register />} />
        <Route path="/mobile/forgot-password" element={<ForgotPassword />} />
        <Route path="/mobile/store-list" element={<StoreList />} />
        <Route path="/mobile/store-detail/:id" element={<StoreDetail />} />
        <Route path="/mobile/dashboard" element={<Dashboard />} />
        <Route path="/mobile/ai-analysis" element={<AIAnalysis />} />
        <Route path="/mobile/insights" element={<Insights />} />
        <Route path="/mobile/negative-reply" element={<NegativeReply />} />
        <Route path="/mobile/positive-activation" element={<PositiveActivation />} />
        <Route path="/mobile/review-stream" element={<ReviewStream />} />
        <Route path="/mobile/review-detail/:id" element={<ReviewDetail />} />
        <Route path="/mobile/platform-detail/:platform" element={<PlatformDetail />} />
        <Route path="/mobile/annual-report" element={<MobileAnnualReport />} />
        <Route path="/mobile/competitor-analysis" element={<MobileCompetitorAnalysis />} />
        <Route path="/mobile/settings" element={<Settings />} />
        <Route path="/mobile/store-settings" element={<StoreSettings />} />
        <Route path="/mobile/reply-template" element={<ReplyTemplate />} />
        <Route path="/mobile/platform-connection" element={<PlatformConnection />} />
        <Route path="/mobile/notification-settings" element={<NotificationSettings />} />
        <Route path="/mobile/auto-reply-settings" element={<AutoReplySettings />} />
        <Route path="/mobile/help-center" element={<HelpCenter />} />
        <Route path="/mobile/subscription" element={<Subscription />} />
        <Route path="/mobile/dish-elimination" element={<DishElimination />} />
        <Route path="/mobile/traceability-detail/:reportId" element={<TraceabilityDetail />} />
        
        {/* ==================== 管理员路由（仅限HQ） ==================== */}
        <Route path="/admin" element={<AdminLogin />} />
        <Route path="/admin/dashboard" element={<AdminGuard><AdminDashboard /></AdminGuard>} />
        
        {/* 管理员 - 主要功能 */}
        <Route path="/admin/ai-config" element={<AdminGuard><AIConfig /></AdminGuard>} />
        <Route path="/admin/competitor-analysis" element={<AdminGuard><CompetitorAnalysis /></AdminGuard>} />
        <Route path="/admin/notification-config" element={<AdminGuard><NotificationConfig /></AdminGuard>} />
        <Route path="/admin/permission-management" element={<AdminGuard><PermissionManagement /></AdminGuard>} />
        <Route path="/admin/reply-audit" element={<AdminGuard><ReplyAudit /></AdminGuard>} />
        <Route path="/admin/review-management" element={<AdminGuard><ReviewManagement /></AdminGuard>} />
        <Route path="/admin/spider-management" element={<AdminGuard><SpiderManagement /></AdminGuard>} />
        <Route path="/admin/store-management" element={<AdminGuard><StoreManagement /></AdminGuard>} />
        <Route path="/admin/annual-report" element={<AdminGuard><AnnualReport /></AdminGuard>} />
        <Route path="/admin/xiaohongshu" element={<AdminGuard><XiaohongshuPage /></AdminGuard>} />
        <Route path="/admin/xiaohongshu-analysis" element={<AdminGuard><XiaohongshuAnalysis /></AdminGuard>} />
        {/* 新增：后台管理缺失的5个功能模块 */}
        <Route path="/admin/negative-reply" element={<AdminGuard><AdminNegativeReply /></AdminGuard>} />
        <Route path="/admin/positive-activation" element={<AdminGuard><AdminPositiveActivation /></AdminGuard>} />
        <Route path="/admin/insights" element={<AdminGuard><AdminInsights /></AdminGuard>} />
        <Route path="/admin/ai-analysis" element={<AdminGuard><AdminAIAnalysis /></AdminGuard>} />
        <Route path="/admin/mobile-settings" element={<AdminGuard><AdminMobileSettings /></AdminGuard>} />
        
        {/* 管理员 - AI配置子页面 */}
        <Route path="/admin/ai-config/evaluation" element={<AdminGuard><Evaluation /></AdminGuard>} />
        <Route path="/admin/ai-config/model" element={<AdminGuard><ModelConfig /></AdminGuard>} />
        <Route path="/admin/ai-config/monitoring" element={<AdminGuard><Monitoring /></AdminGuard>} />
        <Route path="/admin/ai-config/prompts" element={<AdminGuard><PromptConfig /></AdminGuard>} />
        <Route path="/admin/ai-config/rules" element={<AdminGuard><RuleEngine /></AdminGuard>} />
        
        {/* 404 */}
        <Route path="*" element={<div>404 - 页面不存在</div>} />
      </Routes>
      <Toaster toasts={toasts} removeToast={removeToast} />
    </>
  );
}

function App() {
  return (
    <ToastProvider>
      <AppContent />
    </ToastProvider>
  );
}

export default App;
