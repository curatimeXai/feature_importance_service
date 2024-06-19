import LocalView from "@/views/LocalView.vue";
import GlobalView from "@/views/GlobalView.vue";
import SettingsView from "@/views/SettingsView.vue";
import TutorialView from "@/views/TutorialView.vue";

export const routes = [
    {path: '/', component: LocalView},
    {path: '/global', component: GlobalView},
    {path: '/settings', component: SettingsView},
    {path: '/tutorial', component: TutorialView},
]
