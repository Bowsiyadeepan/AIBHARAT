'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  PhotoIcon, 
  DocumentTextIcon,
  EnvelopeIcon,
  ArrowRightIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import toast from 'react-hot-toast';

import { useContentGeneration } from '@/hooks/useContentGeneration';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Button } from '@/components/ui/Button';
import { Select } from '@/components/ui/Select';
import { TextArea } from '@/components/ui/TextArea';

const contentGenerationSchema = z.object({
  prompt: z.string().min(10, 'Prompt must be at least 10 characters'),
  contentType: z.enum(['social_post', 'blog_post', 'email', 'ad_copy']),
  platform: z.string().optional(),
  tone: z.enum(['professional', 'casual', 'friendly', 'authoritative', 'conversational']),
  includeHashtags: z.boolean().default(false),
  includeCta: z.boolean().default(false)
});

type ContentGenerationForm = z.infer<typeof contentGenerationSchema>;

const contentTypes = [
  { value: 'social_post', label: 'Social Media Post', icon: SparklesIcon },
  { value: 'blog_post', label: 'Blog Article', icon: DocumentTextIcon },
  { value: 'email', label: 'Email Campaign', icon: EnvelopeIcon },
  { value: 'ad_copy', label: 'Ad Copy', icon: PhotoIcon }
];

const platforms = [
  { value: 'linkedin', label: 'LinkedIn' },
  { value: 'twitter', label: 'Twitter' },
  { value: 'facebook', label: 'Facebook' },
  { value: 'instagram', label: 'Instagram' }
];

const tones = [
  { value: 'professional', label: 'Professional' },
  { value: 'casual', label: 'Casual' },
  { value: 'friendly', label: 'Friendly' },
  { value: 'authoritative', label: 'Authoritative' },
  { value: 'conversational', label: 'Conversational' }
];

export function ContentGenerationWidget() {
  const [generatedContent, setGeneratedContent] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  
  const { generateContent, isLoading } = useContentGeneration();
  
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
    reset
  } = useForm<ContentGenerationForm>({
    resolver: zodResolver(contentGenerationSchema),
    defaultValues: {
      contentType: 'social_post',
      tone: 'professional',
      includeHashtags: false,
      includeCta: false
    }
  });

  const selectedContentType = watch('contentType');
  const selectedPlatform = watch('platform');

  const onSubmit = async (data: ContentGenerationForm) => {
    try {
      setIsGenerating(true);
      setGeneratedContent(null);

      const result = await generateContent({
        prompt: data.prompt,
        content_type: data.contentType,
        platform: data.platform,
        tone: data.tone,
        include_hashtags: data.includeHashtags,
        include_cta: data.includeCta,
        max_length: getMaxLength(data.contentType)
      });

      setGeneratedContent(result.generated_text);
      toast.success('Content generated successfully!');
      
    } catch (error) {
      console.error('Content generation failed:', error);
      toast.error('Failed to generate content. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const getMaxLength = (contentType: string): number => {
    const limits = {
      social_post: 280,
      blog_post: 4000,
      email: 2000,
      ad_copy: 150
    };
    return limits[contentType as keyof typeof limits] || 280;
  };

  const handleUseContent = () => {
    if (generatedContent) {
      // Navigate to content editor or save content
      toast.success('Content saved to drafts!');
      setGeneratedContent(null);
      reset();
    }
  };

  const handleRegenerate = () => {
    handleSubmit(onSubmit)();
  };

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Content Type Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Content Type
          </label>
          <div className="grid grid-cols-2 gap-3">
            {contentTypes.map((type) => {
              const Icon = type.icon;
              return (
                <label
                  key={type.value}
                  className={`
                    relative flex items-center p-3 rounded-lg border cursor-pointer transition-colors
                    ${selectedContentType === type.value
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:bg-gray-50'
                    }
                  `}
                >
                  <input
                    type="radio"
                    value={type.value}
                    {...register('contentType')}
                    className="sr-only"
                  />
                  <Icon className="w-5 h-5 text-gray-600 mr-2" />
                  <span className="text-sm font-medium text-gray-900">
                    {type.label}
                  </span>
                  {selectedContentType === type.value && (
                    <CheckCircleIcon className="w-5 h-5 text-blue-500 ml-auto" />
                  )}
                </label>
              );
            })}
          </div>
        </div>

        {/* Platform Selection (for social posts) */}
        {selectedContentType === 'social_post' && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Platform
            </label>
            <Select
              {...register('platform')}
              options={platforms}
              placeholder="Select platform"
            />
          </div>
        )}

        {/* Prompt Input */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Content Prompt
          </label>
          <TextArea
            {...register('prompt')}
            placeholder="Describe what you want to create... (e.g., 'Write a LinkedIn post about AI productivity tools')"
            rows={3}
            error={errors.prompt?.message}
          />
        </div>

        {/* Tone Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tone
          </label>
          <Select
            {...register('tone')}
            options={tones}
          />
        </div>

        {/* Additional Options */}
        <div className="flex items-center space-x-6">
          <label className="flex items-center">
            <input
              type="checkbox"
              {...register('includeHashtags')}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="ml-2 text-sm text-gray-700">Include hashtags</span>
          </label>
          
          <label className="flex items-center">
            <input
              type="checkbox"
              {...register('includeCta')}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="ml-2 text-sm text-gray-700">Include call-to-action</span>
          </label>
        </div>

        {/* Generate Button */}
        <Button
          type="submit"
          disabled={isGenerating || isLoading}
          className="w-full"
        >
          {isGenerating ? (
            <>
              <LoadingSpinner size="sm" className="mr-2" />
              Generating...
            </>
          ) : (
            <>
              <SparklesIcon className="w-5 h-5 mr-2" />
              Generate Content
            </>
          )}
        </Button>
      </form>

      {/* Generated Content Display */}
      {generatedContent && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gray-50 rounded-lg p-4 border border-gray-200"
        >
          <div className="flex items-center justify-between mb-3">
            <h4 className="text-sm font-medium text-gray-900">Generated Content</h4>
            <div className="flex items-center text-xs text-gray-500">
              <ClockIcon className="w-4 h-4 mr-1" />
              Just now
            </div>
          </div>
          
          <div className="bg-white rounded-md p-3 border border-gray-200 mb-4">
            <p className="text-gray-900 whitespace-pre-wrap">{generatedContent}</p>
          </div>
          
          <div className="flex items-center space-x-3">
            <Button
              onClick={handleUseContent}
              size="sm"
              className="flex-1"
            >
              <CheckCircleIcon className="w-4 h-4 mr-2" />
              Use This Content
            </Button>
            
            <Button
              onClick={handleRegenerate}
              variant="outline"
              size="sm"
              disabled={isGenerating}
            >
              {isGenerating ? (
                <LoadingSpinner size="sm" />
              ) : (
                'Regenerate'
              )}
            </Button>
          </div>
        </motion.div>
      )}

      {/* Quick Tips */}
      <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
        <h4 className="text-sm font-medium text-blue-900 mb-2">💡 Quick Tips</h4>
        <ul className="text-xs text-blue-800 space-y-1">
          <li>• Be specific about your target audience and goals</li>
          <li>• Include relevant keywords or topics you want to cover</li>
          <li>• Mention the desired length or format if specific</li>
          <li>• Try different tones to match your brand voice</li>
        </ul>
      </div>
    </div>
  );
}