export default {
  title: 'Purepy',
  description: 'A Python Template Engine inspired by ReactJS',
  base: '/purepy/',
  defaultLocale: 'en-US',
  locales: {
    root: {
      label: 'English',
      lang: 'en-US',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/' },
          { text: 'Guide', link: '/guide/' },
          { text: 'API', link: '/api/' }
        ]
      }
    },
    zh: {
      label: '简体中文',
      lang: 'zh-CN',
      themeConfig: {
        nav: [
          { text: '首页', link: '/zh/' },
          { text: '指南', link: '/zh/guide/' },
          { text: 'API', link: '/zh/api/' }
        ]
      }
    }
  },
  themeConfig: {
    sidebar: {
      '/guide/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Introduction', link: '/guide/introduction' },
            { text: 'What is Purepy?', link: '/guide/' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Getting Started', link: '/guide/getting-started' }
          ]
        },
        {
          text: 'Basics',
          items: [
            { text: 'Core Concepts', link: '/guide/concepts' },
            { text: 'Basic Usage', link: '/guide/basic-usage' },
            { text: 'Utility Functions', link: '/guide/utils' },
            { text: 'Components', link: '/guide/components' },
            { text: 'Props and Slots', link: '/guide/props' }
          ]
        },
        {
          text: 'Building the Interface',
          items: [
            { text: 'Compiled Rendering', link: '/guide/compiled' },
            { text: 'Artifacts & Deployment', link: '/guide/artifacts' }
          ]
        },
        {
          text: 'Support',
          items: [
            { text: 'Troubleshooting', link: '/guide/troubleshooting' },
            { text: 'Upgrading', link: '/guide/upgrading' }
          ]
        },
        {
          text: 'Integration',
          items: [
            { text: 'Examples', link: '/guide/examples' },
            { text: 'HTMX Integration', link: '/guide/htmx' },
            { text: 'Events', link: '/guide/events' },
            { text: 'Flask Integration', link: '/guide/flask' },
            { text: 'Django Integration', link: '/guide/django' },
            { text: 'TailwindCSS Integration', link: '/guide/tailwindcss' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API Reference',
          items: [
            { text: 'Overview', link: '/api/' },
            { text: 'Component API', link: '/api/component' },
            { text: 'Compile API', link: '/api/compile' },
            { text: 'Core Classes', link: '/api/core' },
            { text: 'HTML Class', link: '/api/html' },
            { text: 'HTML Tags', link: '/api/html-tags' },
            { text: 'SVG Class', link: '/api/svg' },
            { text: 'SVG Tags', link: '/api/svg-tags' },
            { text: 'XML Class', link: '/api/xml' }
          ]
        }
      ],
      '/zh/guide/': [
        {
          text: '介绍',
          items: [
            { text: '简介', link: '/zh/guide/introduction' },
            { text: '什么是 Purepy?', link: '/zh/guide/' },
            { text: '安装', link: '/zh/guide/installation' },
            { text: '快速开始', link: '/zh/guide/getting-started' }
          ]
        },
        {
          text: '基础',
          items: [
            { text: '基本概念', link: '/zh/guide/concepts' },
            { text: '基本用法', link: '/zh/guide/basic-usage' },
            { text: '工具函数', link: '/zh/guide/utils' },
            { text: '组件', link: '/zh/guide/components' },
            { text: '属性', link: '/zh/guide/props' }
          ]
        },
        {
          text: '构建界面',
          items: [
            { text: '编译渲染', link: '/zh/guide/compiled' },
            { text: '产物与部署', link: '/zh/guide/artifacts' }
          ]
        },
        {
          text: '支持',
          items: [
            { text: '故障排查', link: '/zh/guide/troubleshooting' },
            { text: '升级指南', link: '/zh/guide/upgrading' }
          ]
        },
        {
          text: '集成',
          items: [
            { text: '示例', link: '/zh/guide/examples' },
            { text: 'HTMX 集成', link: '/zh/guide/htmx' },
            { text: '事件', link: '/zh/guide/events' },
            { text: 'Flask 集成', link: '/zh/guide/flask' },
            { text: 'Django 集成', link: '/zh/guide/django' },
            { text: 'TailwindCSS 集成', link: '/zh/guide/tailwindcss' }
          ]
        }
      ],
      '/zh/api/': [
        {
          text: 'API 参考',
          items: [
            { text: '概览', link: '/zh/api/' },
            { text: '组件 API', link: '/zh/api/component' },
            { text: '编译 API', link: '/zh/api/compile' },
            { text: 'Tag 类', link: '/zh/api/tag' },
            { text: 'Raw 类', link: '/zh/api/raw' },
            { text: '核心类', link: '/zh/api/core' },
            { text: 'HTML 类', link: '/zh/api/html' },
            { text: 'HTML 标签', link: '/zh/api/html-tags' },
            { text: 'SVG 类', link: '/zh/api/svg' },
            { text: 'SVG 标签', link: '/zh/api/svg-tags' },
            { text: 'XML 类', link: '/zh/api/xml' }
          ]
        }
      ]
    },
    footer: {
      message: 'Released under the MIT License',
      copyright: 'Copyright © 2024-present Purepy'
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/YonLD/purepy' }
    ],
    search: {
      provider: 'local'
    },
    langMenuLabel: 'Change language',
    returnToTopLabel: 'Back to top'
  }
}
