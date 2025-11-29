'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

interface Employee {
  id: string;
  full_name: string;
  job_title?: string;
  email?: string;
  phone?: string;
  whatsapp?: string;
  bio?: string;
  photo_url?: string;
  public_slug: string;
  company_slug?: string;
  social_links?: Record<string, string>;
}

interface EmployeeFormState {
  full_name: string;
  job_title: string;
  email: string;
  phone: string;
  whatsapp: string;
  bio: string;
  photo_url: string;
  social_links: {
    instagram: string;
    linkedin: string;
    facebook: string;
    youtube: string;
  };
}

interface Subscription {
  plan_name: string;
  status: string;
  employee_limit: number;
  current_employee_count: number;
  trial_end?: string;
}

const emptyEmployee: EmployeeFormState = {
  full_name: '',
  job_title: '',
  email: '',
  phone: '',
  whatsapp: '',
  bio: '',
  photo_url: '',
  social_links: {
    instagram: '',
    linkedin: '',
    facebook: '',
    youtube: '',
  },
};

export default function AdminDashboardPage() {
  const router = useRouter();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState<EmployeeFormState>(emptyEmployee);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [subscription, setSubscription] = useState<Subscription | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const companyId = localStorage.getItem('company_id');

    if (!token || !companyId) {
      router.push('/auth/login');
      return;
    }

    fetchEmployees(token, companyId);
    fetchSubscription(token);
  }, []);

  const fetchSubscription = async (token: string) => {
    try {
      const response = await axios.get('/api/proxy?path=/api/subscriptions/current', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSubscription(response.data);
    } catch (error) {
      console.error('Failed to fetch subscription:', error);
    }
  };

  const fetchEmployees = async (token: string, companyId: string) => {
    try {
      const response = await axios.get(
        `/api/proxy?path=/company/${companyId}/employees`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setEmployees(response.data);
    } catch (error) {
      console.error('Failed to fetch employees:', error);
      setError('Failed to load employees');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenForm = (employee?: Employee) => {
    if (employee) {
      setEditingId(employee.id);
      setFormData({
        full_name: employee.full_name,
        job_title: employee.job_title || '',
        email: employee.email || '',
        phone: employee.phone || '',
        whatsapp: employee.whatsapp || '',
        bio: employee.bio || '',
        photo_url: employee.photo_url || '',
        social_links: employee.social_links || emptyEmployee.social_links,
      });
    } else {
      setEditingId(null);
      setFormData(emptyEmployee);
    }
    setShowForm(true);
    setError('');
  };

  const handleCloseForm = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData(emptyEmployee);
    setError('');
  };

  const handleSaveEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const companyId = localStorage.getItem('company_id');

    if (!token || !companyId) {
      setError('Authentication required');
      return;
    }

    try {
      if (editingId) {
        // Update existing employee
        await axios.put(
          `/api/proxy?path=/employees/${editingId}`,
          formData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setSuccess('Employee updated successfully');
      } else {
        // Create new employee
        await axios.post(
          `/api/proxy?path=/company/${companyId}/employees`,
          formData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setSuccess('Employee added successfully');
      }

      handleCloseForm();
      await fetchEmployees(token, companyId);

      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save employee');
    }
  };

  const handleDeleteEmployee = async (employeeId: string) => {
    const token = localStorage.getItem('token');

    if (!token) {
      setError('Authentication required');
      return;
    }

    if (!window.confirm('Are you sure you want to delete this employee?')) {
      return;
    }

    try {
      await axios.delete(
        `/api/proxy?path=/employees/${employeeId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setSuccess('Employee deleted successfully');
      const companyId = localStorage.getItem('company_id');
      if (companyId) {
        await fetchEmployees(token, companyId);
      }
      setTimeout(() => setSuccess(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete employee');
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    router.push('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <div className="flex gap-3">
            <a
              href="/company-admin/subscription"
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
            >
              💳 Subscription
            </a>
            <a
              href="/company-admin/settings"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
            >
              ⚙️ Company Settings
            </a>
            <a
              href="/company-admin/branding"
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold"
            >
              🎨 Brand Settings
            </a>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-12">
        {/* Subscription Status Card */}
        {subscription && (
          <div className="mb-8 bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-lg font-semibold mb-2">
                  Current Plan: <span className="text-blue-600">{subscription.plan_name.charAt(0).toUpperCase() + subscription.plan_name.slice(1)}</span>
                </h2>
                <div className="flex items-center gap-4">
                  <div>
                    <span className="text-sm text-gray-600">Employees: </span>
                    <span className="font-semibold">
                      {subscription.current_employee_count} / {subscription.employee_limit === -1 ? '∞' : subscription.employee_limit}
                    </span>
                  </div>
                  {subscription.employee_limit !== -1 && (
                    <div className="flex-1 max-w-xs">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            (subscription.current_employee_count / subscription.employee_limit) * 100 >= 90
                              ? 'bg-red-500'
                              : (subscription.current_employee_count / subscription.employee_limit) * 100 >= 70
                              ? 'bg-yellow-500'
                              : 'bg-green-500'
                          }`}
                          style={{
                            width: `${Math.min((subscription.current_employee_count / subscription.employee_limit) * 100, 100)}%`
                          }}
                        ></div>
                      </div>
                    </div>
                  )}
                  {subscription.trial_end && new Date(subscription.trial_end) > new Date() && (
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full">
                      Trial Active
                    </span>
                  )}
                </div>
                {subscription.employee_limit !== -1 && 
                 subscription.current_employee_count >= subscription.employee_limit && (
                  <p className="mt-3 text-sm text-red-600 font-semibold">
                    ⚠️ You've reached your employee limit. Upgrade your plan to add more employees.
                  </p>
                )}
              </div>
              {subscription.plan_name !== 'enterprise' && (
                <a
                  href="/pricing"
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
                >
                  Upgrade Plan
                </a>
              )}
            </div>
          </div>
        )}

        {/* Success/Error Messages */}
        {success && (
          <div className="mb-4 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
            {success}
          </div>
        )}
        {error && (
          <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Add/Edit Employee Button */}
        {!showForm && (
          <div className="mb-8">
            <button
              onClick={() => handleOpenForm()}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
              disabled={subscription && subscription.employee_limit !== -1 && subscription.current_employee_count >= subscription.employee_limit}
            >
              + Add Employee
            </button>
            {subscription && subscription.employee_limit !== -1 && subscription.current_employee_count >= subscription.employee_limit && (
              <span className="ml-3 text-sm text-red-600">
                Upgrade your plan to add more employees
              </span>
            )}

          </div>
        )}

        {/* Add/Edit Employee Form */}
        {showForm && (
          <div className="bg-white rounded-lg shadow mb-8 p-6">
            <h2 className="text-xl font-bold mb-4">
              {editingId ? 'Edit Employee' : 'Add New Employee'}
            </h2>
            <form onSubmit={handleSaveEmployee} className="space-y-4">
              {/* Basic Information */}
              <div className="border-b pb-4">
                <h3 className="font-semibold text-gray-700 mb-3">Basic Information</h3>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Full Name *
                  </label>
                  <input
                    type="text"
                    value={formData.full_name}
                    onChange={(e) =>
                      setFormData({ ...formData, full_name: e.target.value })
                    }
                    required
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    Job Title
                  </label>
                  <input
                    type="text"
                    value={formData.job_title}
                    onChange={(e) =>
                      setFormData({ ...formData, job_title: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    Bio
                  </label>
                  <textarea
                    value={formData.bio}
                    onChange={(e) =>
                      setFormData({ ...formData, bio: e.target.value })
                    }
                    placeholder="Brief description or bio"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 h-20"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    Photo URL
                  </label>
                  <input
                    type="url"
                    value={formData.photo_url}
                    onChange={(e) =>
                      setFormData({ ...formData, photo_url: e.target.value })
                    }
                    placeholder="https://example.com/photo.jpg"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>
              </div>

              {/* Contact Information */}
              <div className="border-b pb-4">
                <h3 className="font-semibold text-gray-700 mb-3">Contact Information</h3>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Email
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) =>
                      setFormData({ ...formData, email: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    Phone
                  </label>
                  <input
                    type="tel"
                    value={formData.phone}
                    onChange={(e) =>
                      setFormData({ ...formData, phone: e.target.value })
                    }
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    WhatsApp
                  </label>
                  <input
                    type="tel"
                    value={formData.whatsapp}
                    onChange={(e) =>
                      setFormData({ ...formData, whatsapp: e.target.value })
                    }
                    placeholder="+1 (555) 000-0000"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>
              </div>

              {/* Social Media Links */}
              <div className="pb-4">
                <h3 className="font-semibold text-gray-700 mb-3">Social Media Links</h3>
                <p className="text-sm text-gray-500 mb-3">Enter full profile URLs (all optional)</p>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    📷 Instagram
                  </label>
                  <input
                    type="url"
                    value={formData.social_links.instagram}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        social_links: { ...formData.social_links, instagram: e.target.value },
                      })
                    }
                    placeholder="https://instagram.com/username"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    💼 LinkedIn
                  </label>
                  <input
                    type="url"
                    value={formData.social_links.linkedin}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        social_links: { ...formData.social_links, linkedin: e.target.value },
                      })
                    }
                    placeholder="https://linkedin.com/in/username"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    👍 Facebook
                  </label>
                  <input
                    type="url"
                    value={formData.social_links.facebook}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        social_links: { ...formData.social_links, facebook: e.target.value },
                      })
                    }
                    placeholder="https://facebook.com/username"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>

                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700">
                    🎬 YouTube
                  </label>
                  <input
                    type="url"
                    value={formData.social_links.youtube}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        social_links: { ...formData.social_links, youtube: e.target.value },
                      })
                    }
                    placeholder="https://youtube.com/@username"
                    className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold"
                >
                  {editingId ? 'Update Employee' : 'Add Employee'}
                </button>
                <button
                  type="button"
                  onClick={handleCloseForm}
                  className="flex-1 px-4 py-3 bg-gray-400 text-white rounded-lg hover:bg-gray-500 font-semibold"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Employees List */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-bold">Employees ({employees.length})</h2>
          </div>

          {loading ? (
            <div className="p-6 text-center text-gray-500">Loading...</div>
          ) : employees.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              No employees yet. Add one to get started!
            </div>
          ) : (
            <div className="divide-y">
              {employees.map((employee) => (
                <div key={employee.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">
                        {employee.full_name}
                      </h3>
                      <p className="text-sm text-gray-600">{employee.job_title}</p>
                      {employee.email && (
                        <p className="text-sm text-gray-600">{employee.email}</p>
                      )}
                    </div>
                    <div className="flex gap-2 ml-4">
                      <button
                        onClick={() => handleOpenForm(employee)}
                        className="px-3 py-2 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
                      >
                        ✏️ Edit
                      </button>
                      <button
                        onClick={() => handleDeleteEmployee(employee.id)}
                        className="px-3 py-2 bg-red-500 text-white text-sm rounded hover:bg-red-600"
                      >
                        🗑️ Delete
                      </button>
                      <a
                        href={`/card/${employee.company_slug || 'your-company'}/${employee.public_slug}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-3 py-2 bg-green-500 text-white text-sm rounded hover:bg-green-600"
                      >
                        👁️ View
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
