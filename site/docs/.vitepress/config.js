export default {
  title: 'Purepy',
  description: 'A Python Template Engine inspired by ReactJS',
  base: '/purepy/',
  defaultLocale: 'zh-CN',
  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN',
      themeConfig: {
        nav: [
          { text: '首页', link: '/' },
          { text: '指南', link: '/guide/' },
          { text: 'API', link: '/api/' }
        ]
      }
    },
    en: {
      label: 'English',
      lang: 'en-US',
      themeConfig: {
        nav: [
          { text: 'Home', link: '/en/' },
          { text: 'Guide', link: '/en/guide/' },
          { text: 'API', link: '/en/api/' }
        ]
      }
    }
  },
  themeConfig: {
    sidebar: {
      '/guide/': [
        {
          text: '介绍',
          items: [
            { text: '简介', link: '/guide/introduction' },
            { text: '什么是 Purepy?', link: '/guide/' },
            { text: '安装', link: '/guide/installation' },
            { text: '快速开始', link: '/guide/getting-started' }
          ]
        },
        {
          text: '基础',
          items: [
            { text: '基本概念', link: '/guide/concepts' },
            { text: '基本用法', link: '/guide/basic-usage' },
            { text: '工具函数', link: '/guide/utils' },
            { text: '组件', link: '/guide/components' },
            { text: '属性', link: '/guide/props' }
          ]
        },
        {
          text: '集成',
          items: [
            { text: 'Flask 集成', link: '/guide/flask' },
            { text: 'Django 集成', link: '/guide/django' },
            { text: 'TailwindCSS 集成', link: '/guide/tailwindcss' }
          ]
        }
      ],
      '/api/': [
        {
          text: 'API 参考',
          items: [
            { text: 'API 参考', link: '/api/' },
            { text: '核心类', link: '/api/core' },
            { text: 'HTML 标签', link: '/api/html-tags' },
            { text: 'SVG 标签', link: '/api/svg-tags' }
          ]
        }
      ],
      '/en/guide/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Introduction', link: '/en/guide/introduction' },
            { text: 'What is Purepy?', link: '/en/guide/' },
            { text: 'Installation', link: '/en/guide/installation' },
            { text: 'Getting Started', link: '/en/guide/getting-started' }
          ]
        },
        {
          text: 'Basics',
          items: [
            { text: 'Core Concepts', link: '/en/guide/concepts' },
            { text: 'Basic Usage', link: '/en/guide/basic-usage' },
            { text: 'Utility Functions', link: '/en/guide/utils' },
            { text: 'Components', link: '/en/guide/components' },
            { text: 'Props', link: '/en/guide/props' }
          ]
        },
        {
          text: 'Integration',
          items: [
            { text: 'Flask Integration', link: '/en/guide/flask' },
            { text: 'Django Integration', link: '/en/guide/django' },
            { text: 'TailwindCSS Integration', link: '/en/guide/tailwindcss' }
          ]
        }
      ],
      '/en/api/': [
        {
          text: 'API Reference',
          items: [
            { text: 'API Reference', link: '/en/api/' },
            { text: 'Core Classes', link: '/en/api/core' },
            { text: 'HTML Tags', link: '/en/api/html-tags' },
            { text: 'SVG Tags', link: '/en/api/svg-tags' }
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
