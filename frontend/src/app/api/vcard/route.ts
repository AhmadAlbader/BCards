import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const company_slug = searchParams.get('company_slug');
  const employee_slug = searchParams.get('employee_slug');

  if (!company_slug || !employee_slug) {
    return NextResponse.json(
      { error: 'Missing parameters' },
      { status: 400 }
    );
  }

  try {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL 
      ? `${process.env.NEXT_PUBLIC_API_URL}/card/${company_slug}/${employee_slug}/vcard`
      : `http://localhost:8000/api/card/${company_slug}/${employee_slug}/vcard`;
    
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'text/vcard',
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: `Backend returned ${response.status}` },
        { status: response.status }
      );
    }

    const data = await response.text();
    
    // Return as downloadable vCard file
    return new NextResponse(data, {
      status: 200,
      headers: {
        'Content-Type': 'text/vcard',
        'Content-Disposition': `attachment; filename="${company_slug}-${employee_slug}.vcf"`,
      },
    });
  } catch (error) {
    console.error('vCard API route error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch vCard' },
      { status: 500 }
    );
  }
}
