const app = {
    data() {
        return {
            busca: '',
            clientes: []
        }
    },
    watch: {
        busca() {
            this.busca.trim() ? this.faz_busca() : null
        }
    },
    methods: {
        faz_busca: _.debounce(function () {
            axios
                .get(
                    urlBusca //substitui pela url de busca
                    +
                    this.busca.trim())
                .then(response => {
                    this.clientes = response.data.clientes
                })
                .catch(error => {
                    alert('Erro! Não foi possível adquirir resultados da API: ' + error)
                })

        }, 550),
        get_clientes() {
            axios
                .get(
                    urlLista //substitui pela url de busca
                )
                .then(response => {
                    this.clientes = response.data.data
                })
                .catch(error => {
                    alert('Erro! Não foi possível adquirir resultados da API: ' + error)
                })
        }
    },
    created() {
        this.get_clientes()
    },

}
const vm = Vue.createApp(app)
const h = Vue.h
vm.config.compilerOptions.delimiters = ['@{', '}']
vm.component('cliente-item', {
            props: ["cliente"],

            data() {
                return {
                    show: false
                }
            },
            render() {
                return h(
                    'li', {
                        class: 'collapse border rounded-box border-base-content collapse-arrow text-base-content'
                    },
                    [
                        h('input', {
                            type: "checkbox"
                        }),
                        h('div', {
                            class: "collapse-title text-xl font-medium flex"
                        }, [

                            h('div', {
                                class: ""
                            }, [
                                h('div', {
                                    class: " "
                                }, [
                                    h('img', {
                                        src: 'https://avatars.dicebear.com/api/gridy/' + this.cliente.nome + '.svg'
                                    })
                                ]),
                                h('span', {
                                    class: "my-auto px-1"
                                }, this.cliente.nome)
                            ]),
                            h('div', {
                                class: "flex"
                            }) // ????????? apagar???
                        ]),
                        h('div', {
                            class: "collapse-content"
                        }, [
                            h('div', {
                                class: "flex justify-end"
                            }, [
                                h('div', {
                                    class: "indicator"
                                }, [
                                    h('div', {
                                            class: "indicator-item indicator-middle indicator-start badge badge-accent"
                                        },
                                        [this.cliente.projetos.length]),
                                    h('a', {
                                        href: urlCliente + this.cliente.id,
                                        class: "btn btn-outline btn-accent btn-sm align-top collapse-open"
                                    },
                                    ['Projetos'])
                                ]),
                                h('a', {
                                        href: urlNovo + this.cliente.id,
                                        class: "collapse-open btn btn-outline btn-accent btn-sm align-top"
                                    },
                                    ["Novo Projeto"]
                                )
                            ]),
                            h('p', [this.cliente.endereco + '-' + this.cliente.telefone]),
                            h('b', ['Projetos: ']),
                            h('div', {
                                class: 'inline'
                            }, this.cliente.projetos.map((proj) => {
                                return h('span', proj.ambientes.map((amb) => {
                                    return amb.nome + '/'
                                }))
                            }))
                        ])
                    ])
            }
        }
)

        vm.mount("#app")