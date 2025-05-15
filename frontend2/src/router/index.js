import { createRouter, createWebHistory } from 'vue-router';
import JobseekerLogin from '@/views/JobseekerLogin.vue';
import CVForm from '@/views/CVForm.vue';
import MobileLogin from '@/views/MobileLogin.vue';
import JobseekerHomepage from '@/views/JobseekerHomepage.vue';

const routes = [
  { path: '/', component: JobseekerLogin },
  { path: '/cv-form', component: CVForm },
  { path: '/mobile-login', component: MobileLogin },
  { path: '/js-homepage', component: JobseekerHomepage }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
