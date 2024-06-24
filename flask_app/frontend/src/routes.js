import LocalView from "@/views/LocalView.vue";
import GlobalView from "@/views/GlobalView.vue";
import SettingsView from "@/views/SettingsView.vue";
import TutorialView from "@/views/TutorialView.vue";
import ModelSettings from "@/components/Settings/ModelSettings.vue";
import DatasetSettings from "@/components/Settings/DatasetSettings.vue";
import FrequentQuestions from "@/components/Settings/FrequentQuestions.vue";

export const routes = [
    {path: '/', component: LocalView},
    {path: '/global', component: GlobalView},
    {
        path: '/settings', component: SettingsView,
        children: [
            {path: 'model', component: ModelSettings},
            {path: 'dataset', component: DatasetSettings},
            {path: 'questions', component: FrequentQuestions},
        ]
    },
    {path: '/tutorial', component: TutorialView},
]
