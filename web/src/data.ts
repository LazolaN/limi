import type { FarmerOption, Language, Channel } from './types';

export const FARMERS: FarmerOption[] = [
  {
    id: 'farmer-001',
    name: 'Sipho',
    language: 'zu',
    province: 'KwaZulu-Natal',
    farmType: 'Smallholder (4.5 ha)',
    crops: ['maize', 'beans', 'cabbage'],
  },
  {
    id: 'farmer-002',
    name: 'Johan',
    language: 'af',
    province: 'Free State',
    farmType: 'Commercial (850 ha)',
    crops: ['maize', 'soybeans', 'sunflower', 'wheat'],
  },
  {
    id: 'farmer-003',
    name: 'Nomsa',
    language: 'xh',
    province: 'Eastern Cape',
    farmType: 'Emerging (25 ha)',
    crops: ['maize', 'potatoes', 'spinach'],
  },
];

export const LANGUAGES: Array<{ value: Language; label: string }> = [
  { value: 'en', label: 'English' },
  { value: 'zu', label: 'isiZulu' },
  { value: 'xh', label: 'isiXhosa' },
  { value: 'af', label: 'Afrikaans' },
  { value: 'st', label: 'Sesotho' },
];

export const CHANNELS: Array<{ value: Channel; label: string; description: string }> = [
  { value: 'web', label: 'Web', description: 'Rich markdown' },
  { value: 'whatsapp', label: 'WhatsApp', description: '4096 char limit' },
  { value: 'ussd', label: 'USSD', description: '160 char screens' },
  { value: 'ivr', label: 'Voice', description: 'Spoken language' },
  { value: 'sms', label: 'SMS', description: '160 char alerts' },
];

export const QUICK_QUESTIONS = [
  'What is the maize price today?',
  'My tomato leaves have brown spots',
  'When should I plant maize in KZN?',
  'My cow is not eating and has a fever',
  'How do I improve my soil pH?',
  'Ngicela intengo yombila', // isiZulu: maize price
];
