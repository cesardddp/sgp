const App = {
    compilerOptions: {
        delimiters: ['@{', '}']
    },
    data() {
        return {
            projetos: [{
                ambientes: [{
                    id: -1,
                }, ],
                cliente: {
                    nome: "",
                },
                data_apresentacao: "",
                data_entrada: "",
                data_medicao: "",
                fotos: null,
                id: -1,
            }, ]
        }
    },
    methods: {
        detalhes(id) {
            location.pathname = urlIndex + "detalhes/" + id
        }
    },

    mounted() {
        return (
            axios
            .get(urlGetProjetos)
            .then(response => {
                this.projetos = response.data.projetos
            })
        )
    },
}
const app = Vue.createApp(App)
app.component('projeto-row', {
    compilerOptions: {
        delimiters: ['@{', '}']
    },
    props: ['projeto'],
    computed: {
        colorStatus() {
            if (!this.projeto.data_medicao) {
                return "bg-white"
            }
            const data_medicao = new Date(this.projeto.data_medicao);
            const now = new Date();
            const diffTime = Math.abs(data_medicao - now);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            console.log(data_medicao, now)
            if (diffDays >= 7) {
                return "bg-red"
            } else if (diffDays>=15) {
                return "bg-yellow"
            } else {
                return "bg-white"
            }
        }
    },
    template: "#projeto-row"
})
app.mount("#app")