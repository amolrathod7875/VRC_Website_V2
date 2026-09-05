import Link from "next/link";

export default function NotFound() {
  return (
    <div className="mx-auto max-w-xl px-4 py-24 text-center">
      <p className="text-sm font-semibold uppercase tracking-widest text-brand-700">404</p>
      <h1 className="mt-2 text-3xl font-semibold text-brand-950">Page not found</h1>
      <p className="mt-3 text-sm text-slate-600">The page you requested is not in this site map.</p>
      <Link href="/" className="mt-6 inline-flex rounded-md bg-brand-700 px-5 py-2.5 text-sm font-semibold text-white">
        Back to home
      </Link>
    </div>
  );
}
