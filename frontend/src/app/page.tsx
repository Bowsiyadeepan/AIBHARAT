'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { 
  SparklesIcon, 
  ChartBarIcon, 
  ClockIcon, 
  UserGroupIcon,
  ArrowRightIcon,
  PlayIcon
} from '@heroicons/react/24/outline';
import Link from 'next/link';

import { DashboardLayout } from '@/components/layout/DashboardLayout';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { ContentGenerationWidget } from '@/components/dashboard/ContentGenerationWidget';
import { PerformanceChart } from '@/components/dashboard/PerformanceChart';
import { RecentContent } from '@/components/dashboard/RecentContent';
import { UpcomingSchedule } from '@/components/dashboard/UpcomingSchedule';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

const staggerChildren = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

export default function Dashboard() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <motion.div 
          className="flex items-center justify-between"
          {...fadeInUp}
        >
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome back! 👋
            </h1>
            <p className="text-gray-600 mt-1">
              Here's what's happening with your content today
            </p>
          </div>
          
          <div className="flex space-x-3">
            <Link
              href="/content/generate"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <SparklesIcon className="w-5 h-5 mr-2" />
              Generate Content
            </Link>
            
            <button className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
              <PlayIcon className="w-5 h-5 mr-2" />
              Quick Tour
            </button>
          </div>
        </motion.div>

        {/* Metrics Overview */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          variants={staggerChildren}
          initial="initial"
          animate="animate"
        >
          <motion.div variants={fadeInUp}>
            <MetricCard
              title="Content Generated"
              value="1,247"
              change="+12%"
              changeType="positive"
              icon={SparklesIcon}
              description="This month"
            />
          </motion.div>
          
          <motion.div variants={fadeInUp}>
            <MetricCard
              title="Avg. Engagement"
              value="4.2%"
              change="+0.8%"
              changeType="positive"
              icon={ChartBarIcon}
              description="Last 30 days"
            />
          </motion.div>
          
          <motion.div variants={fadeInUp}>
            <MetricCard
              title="Time Saved"
              value="156h"
              change="+23h"
              changeType="positive"
              icon={ClockIcon}
              description="This month"
            />
          </motion.div>
          
          <motion.div variants={fadeInUp}>
            <MetricCard
              title="Reach"
              value="89.2K"
              change="+15.3K"
              changeType="positive"
              icon={UserGroupIcon}
              description="Total reach"
            />
          </motion.div>
        </motion.div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Content Generation */}
          <motion.div 
            className="lg:col-span-2 space-y-8"
            {...fadeInUp}
            transition={{ delay: 0.2 }}
          >
            {/* Quick Content Generation */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Quick Generate
                </h2>
                <Link 
                  href="/content/generate"
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center"
                >
                  Advanced Options
                  <ArrowRightIcon className="w-4 h-4 ml-1" />
                </Link>
              </div>
              <ContentGenerationWidget />
            </div>

            {/* Performance Analytics */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Performance Overview
                </h2>
                <select className="text-sm border border-gray-300 rounded-lg px-3 py-1">
                  <option>Last 7 days</option>
                  <option>Last 30 days</option>
                  <option>Last 90 days</option>
                </select>
              </div>
              <PerformanceChart />
            </div>

            {/* Recent Content */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Recent Content
                </h2>
                <Link 
                  href="/content"
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center"
                >
                  View All
                  <ArrowRightIcon className="w-4 h-4 ml-1" />
                </Link>
              </div>
              <RecentContent />
            </div>
          </motion.div>

          {/* Right Column - Sidebar */}
          <motion.div 
            className="space-y-8"
            {...fadeInUp}
            transition={{ delay: 0.3 }}
          >
            {/* Upcoming Schedule */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Upcoming Posts
                </h2>
                <Link 
                  href="/schedule"
                  className="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center"
                >
                  Manage
                  <ArrowRightIcon className="w-4 h-4 ml-1" />
                </Link>
              </div>
              <UpcomingSchedule />
            </div>

            {/* AI Insights */}
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-200 p-6">
              <div className="flex items-center mb-4">
                <SparklesIcon className="w-6 h-6 text-blue-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">
                  AI Insights
                </h3>
              </div>
              
              <div className="space-y-4">
                <div className="bg-white rounded-lg p-4 border border-blue-100">
                  <p className="text-sm text-gray-700 mb-2">
                    <strong>Best posting time:</strong> Tuesday at 2 PM shows 23% higher engagement
                  </p>
                  <button className="text-blue-600 text-xs font-medium hover:text-blue-700">
                    Schedule content for this time →
                  </button>
                </div>
                
                <div className="bg-white rounded-lg p-4 border border-blue-100">
                  <p className="text-sm text-gray-700 mb-2">
                    <strong>Trending topic:</strong> "AI productivity tools" is gaining traction in your industry
                  </p>
                  <button className="text-blue-600 text-xs font-medium hover:text-blue-700">
                    Generate content about this →
                  </button>
                </div>
                
                <div className="bg-white rounded-lg p-4 border border-blue-100">
                  <p className="text-sm text-gray-700 mb-2">
                    <strong>Content gap:</strong> You haven't posted on LinkedIn in 3 days
                  </p>
                  <button className="text-blue-600 text-xs font-medium hover:text-blue-700">
                    Create LinkedIn post →
                  </button>
                </div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Actions
              </h3>
              
              <div className="space-y-3">
                <Link
                  href="/content/generate?type=social_post"
                  className="block w-full text-left px-4 py-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Social Media Post</div>
                  <div className="text-sm text-gray-600">Quick social content</div>
                </Link>
                
                <Link
                  href="/content/generate?type=blog_post"
                  className="block w-full text-left px-4 py-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Blog Article</div>
                  <div className="text-sm text-gray-600">Long-form content</div>
                </Link>
                
                <Link
                  href="/content/generate?type=email"
                  className="block w-full text-left px-4 py-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">Email Campaign</div>
                  <div className="text-sm text-gray-600">Marketing emails</div>
                </Link>
                
                <Link
                  href="/analytics"
                  className="block w-full text-left px-4 py-3 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  <div className="font-medium text-gray-900">View Analytics</div>
                  <div className="text-sm text-gray-600">Performance insights</div>
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </DashboardLayout>
  );
}