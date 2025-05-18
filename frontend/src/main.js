import { createApp } from 'vue';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Pages
import WelcomePage from './views/WelcomePage.vue';
import LoginPage from './views/LoginPage.vue';
import RegisterPage from './views/RegisterPage.vue';
import DashboardPage from './views/DashboardPage.vue';

//components
import AdminSettings from './components/AdminSettings.vue';
import TestsLists from './components/TestsLists.vue';
import JobseekerAnswers from './components/JobseekerAnswers.vue';
import CVEntries from './components/CVEntries.vue';
import CVPreview from './components/CVPreview.vue';

const routes = [
  { path: '/', component: WelcomePage },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/dashboard', component: DashboardPage },
  { path: '/answers', component: JobseekerAnswers },
  { path: '/cvforms', component: CVEntries },
  { path: '/settings', component: AdminSettings },
  { path: '/tests', component: TestsLists },
   {
    path: '/preview-cv/:id',
    name: 'PreviewCV',
    component: CVPreview,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
