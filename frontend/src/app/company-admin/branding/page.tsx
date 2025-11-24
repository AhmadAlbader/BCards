'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface BrandingData {
  brand_color: string;
  logo_url: string;
  company_name: string;
  slug: string;
}

export default function BrandingPage() {
  const router = useRouter();
  const [brandColor, setBrandColor] = useState('#3B82F6');
  const [logoUrl, setLogoUrl] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [presetColors] = useState([
    '#3B82F6', // Blue
    '#EF4444', // Red
    '#10B981', // Green
    '#F59E0B', // Amber
    '#8B5CF6', // Purple
    '#EC4899', // Pink
    '#06B6D4', // Cyan
    '#6366F1', // Indigo
  ]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const companyId = localStorage.getItem('company_id');

    if (!token || !companyId) {
      router.push('/auth/login');
      return;
    }

    fetchBranding(token, companyId);
  }, []);

  const fetchBranding = async (token: string, companyId: string) => {
    try {
      const response = await axios.get(
        `/api/proxy?path=/company/${companyId}/branding`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      const data: BrandingData = response.data;
      setBrandColor(data.brand_color || '#3B82F6');
      setLogoUrl(data.logo_url || '');
      setCompanyName(data.company_name);
    } catch (err: any) {
      setError('Failed to load branding settings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage('');
    setError('');
    const companyId = localStorage.getItem('company_id');
    const token = localStorage.getItem('token');

    try {
      const response = await axios.put(
        `/api/proxy?path=/company/${companyId}/branding`,
        {
          brand_color: brandColor,
          logo_url: logoUrl,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setMessage('✅ Branding updated successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update branding');
    } finally {
      setSaving(false);
    }
  };

  const handleClearLogo = () => {
    setLogoUrl('');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading branding settings...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Brand Settings</h1>
            <p className="text-gray-600 mt-1">{companyName}</p>
          </div>
          <button
            onClick={() => router.back()}
            className="px-4 py-2 text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg"
          >
            ← Back
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Messages */}
        {message && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg">
            {message}
          </div>
        )}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Settings Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* Brand Color Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4 text-gray-900">Brand Color</h2>
              <p className="text-gray-600 text-sm mb-4">
                This color will be used for card backgrounds, buttons, and accents on digital cards.
              </p>

              <div className="flex gap-4 items-start mb-6">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-gray-700">Color Picker</label>
                  <input
                    type="color"
                    value={brandColor}
                    onChange={(e) => setBrandColor(e.target.value)}
                    className="w-24 h-24 rounded cursor-pointer border-2 border-gray-200 hover:border-gray-300"
                  />
                </div>
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-700 mb-2">Hex Value</label>
                  <input
                    type="text"
                    value={brandColor}
                    onChange={(e) => {
                      const val = e.target.value;
                      if (val.startsWith('#') && (val.length === 7 || val.length === 4)) {
                        setBrandColor(val);
                      }
                    }}
                    placeholder="#3B82F6"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  />
                  <p className="text-xs text-gray-500 mt-1">Format: #RGB or #RRGGBB</p>
                </div>
              </div>

              {/* Preset Colors */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">Or choose a preset</label>
                <div className="grid grid-cols-4 gap-3">
                  {presetColors.map((color) => (
                    <button
                      key={color}
                      onClick={() => setBrandColor(color)}
                      className={`w-full h-12 rounded border-2 transition-all ${
                        brandColor === color ? 'border-gray-900 scale-105' : 'border-gray-300 hover:border-gray-500'
                      }`}
                      style={{ backgroundColor: color }}
                      title={color}
                    />
                  ))}
                </div>
              </div>
            </div>

            {/* Logo Section */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4 text-gray-900">Company Logo</h2>
              <p className="text-gray-600 text-sm mb-4">
                Upload a logo URL. It will appear on digital cards and in the brand preview.
              </p>

              <div className="space-y-4">
                {logoUrl && (
                  <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
                    <img src={logoUrl} alt="Company Logo" className="h-16 w-auto object-contain" />
                    <div className="flex-1">
                      <p className="text-sm text-gray-600 break-all">{logoUrl}</p>
                    </div>
                    <button
                      onClick={handleClearLogo}
                      className="px-3 py-1 text-sm text-red-600 hover:text-red-700 border border-red-200 rounded"
                    >
                      Clear
                    </button>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Logo URL</label>
                  <input
                    type="text"
                    placeholder="https://example.com/logo.png"
                    value={logoUrl}
                    onChange={(e) => setLogoUrl(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <p className="text-xs text-gray-500 mt-1">Must be a publicly accessible image URL (PNG, JPG, GIF)</p>
                </div>
              </div>
            </div>

            {/* Save Button */}
            <div className="flex gap-3">
              <button
                onClick={handleSave}
                disabled={saving}
                className="flex-1 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
              >
                {saving ? '💾 Saving...' : '💾 Save Changes'}
              </button>
              <button
                onClick={() => setLogoUrl('')}
                className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-colors"
              >
                Reset Logo
              </button>
            </div>
          </div>

          {/* Preview Column */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6 sticky top-4">
              <h2 className="text-lg font-semibold mb-4 text-gray-900">Live Preview</h2>

              {/* Card Preview */}
              <div
                className="rounded-lg shadow-lg p-6 text-white mb-4"
                style={{
                  backgroundColor: brandColor,
                  backgroundImage: `linear-gradient(135deg, ${brandColor}dd, ${brandColor})`,
                }}
              >
                <h3 className="text-2xl font-bold mb-1">Sample Card</h3>
                <p className="text-lg opacity-90 mb-4">Employee Name</p>
                <p className="text-sm opacity-75 mb-4">Job Title</p>

                {logoUrl && (
                  <div className="mt-4 pt-4 border-t border-white border-opacity-30">
                    <img src={logoUrl} alt="Logo Preview" className="h-10 w-auto" />
                  </div>
                )}

                {/* Sample QR */}
                <div className="mt-4 flex justify-center bg-white p-2 rounded">
                  <div
                    className="w-16 h-16"
                    style={{
                      background: 'url("data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E%3Crect fill=%27%23000%27 x=%270%27 y=%270%27 width=%2730%27 height=%2730%27/%3E%3Crect fill=%27%23fff%27 x=%275%27 y=%275%27 width=%2720%27 height=%2720%27/%3E%3C/svg%3E")',
                      backgroundSize: 'cover',
                    }}
                  />
                </div>
              </div>

              {/* Hex Code Display */}
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Current Color</p>
                <p className="font-mono font-bold text-gray-900">{brandColor}</p>
              </div>

              {/* Logo URL Display */}
              {logoUrl && (
                <div className="bg-gray-50 p-4 rounded-lg mt-3">
                  <p className="text-xs text-gray-600 mb-1">Logo Status</p>
                  <p className="text-sm text-green-600">✅ Logo Loaded</p>
                </div>
              )}

              {/* Color Impact Info */}
              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-xs font-semibold text-blue-900 mb-2">💡 This color will appear on:</p>
                <ul className="text-xs text-blue-800 space-y-1">
                  <li>✓ Card backgrounds</li>
                  <li>✓ Button elements</li>
                  <li>✓ Accent borders</li>
                  <li>✓ Headers</li>
                  <li>✓ All employee cards</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
