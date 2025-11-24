'use client';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Digital Business Cards
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Create stunning digital business cards for your team
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/auth/signup"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700"
          >
            Get Started
          </a>
          <a
            href="/auth/login"
            className="px-8 py-3 bg-white text-blue-600 border border-blue-600 rounded-lg font-semibold hover:bg-blue-50"
          >
            Login
          </a>
        </div>
      </div>
    </div>
  );
}
