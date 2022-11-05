#include "Main.h"

DemoApp* DemoApp::StaticObject=NULL;

int APIENTRY wWinMain(_In_ HINSTANCE hInstance, _In_opt_ HINSTANCE hPrevInstance, _In_ LPWSTR IpCmdLine, _In_ int nCmdShow)
{
    if(SUCCEEDED(CoInitialize(NULL)))
    {
        {
            DemoApp app;
            if(SUCCEEDED(app.Initialize(hInstance)))
            {
                app.RunMessageLoop();
            }
        }
        CoUninitialize();
    }
    return 0;
}

DemoApp::DemoApp() :
    m_hwnd(NULL),
    m_pDirect2dFactory(NULL),
    m_pRenderTarget(NULL),
    m_pLightSlateGrayBrush(NULL),
    m_pCornflowerBlueBrush(NULL)
{
}

DemoApp::~DemoApp()
{
    DiscardDeviceResources();
    SafeRelease(&m_pDirect2dFactory);
}

HRESULT DemoApp::Initialize(HINSTANCE hinstance)
{
    HRESULT hr;
    hr = CreateDeviceIndependentResources();

    if (SUCCEEDED(hr))
    {
        WNDCLASSEX wcex = { sizeof(WNDCLASSEX) };
        wcex.style = CS_HREDRAW | CS_VREDRAW;
        wcex.lpfnWndProc = DemoApp::WndProc;
        wcex.cbClsExtra = 0;
        wcex.cbWndExtra = sizeof(LONG_PTR);
        wcex.hInstance = hinstance;
        wcex.hbrBackground = NULL;
        wcex.lpszMenuName = NULL;
        wcex.hCursor = LoadCursor(NULL, IDI_APPLICATION);
        wcex.lpszClassName = L"D2DDemoApp";
        RegisterClassEx(&wcex);

        m_hwnd = CreateWindow(L"D2DDemoApp", L"Direct2D Demo Application",
                              WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT,
                              640, 480, NULL, NULL, hinstance, this);
        hr = m_hwnd ? S_OK : E_FAIL;
        if (SUCCEEDED(hr))
        {
            ShowWindow(m_hwnd, SW_SHOWNORMAL);
            UpdateWindow(m_hwnd);
        }
    }
    return hr;
}

HRESULT DemoApp::CreateDeviceIndependentResources()
{
    HRESULT hr = S_OK;

    hr = D2D1CreateFactory(D2D1_FACTORY_TYPE_SINGLE_THREADED, &m_pDirect2dFactory);

    return hr;
}

HRESULT DemoApp::CreateDeviceResources()
{
    HRESULT hr = S_OK;

    if (m_pRenderTarget)
    {
        RECT rc;
        GetClientRect(m_hwnd, &rc);

        D2D1_SIZE_U size = D2D1::SizeU(rc.right - rc.left, rc.bottom - rc.top);

        hr = m_pDirect2dFactory->CreateHwndRenderTarget(D2D1::RenderTargetProperties(), D2D1::HwndRenderTargetProperties(m_hwnd, size), &m_pRenderTarget);

        if (SUCCEEDED(hr))
        {
            hr = m_pRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::LightSlateGray), &m_pLightSlateGrayBrush);
        }
        if (SUCCEEDED(hr))
        {
            hr = m_pRenderTarget->CreateSolidColorBrush(D2D1::ColorF(D2D1::ColorF::CornflowerBlue), &m_pCornflowerBlueBrush);
        }
    }

    return hr;
}

void DemoApp::DiscardDeviceResources()
{
    SafeRelease(&m_pDirect2dFactory);
    SafeRelease(&m_pRenderTarget);
    SafeRelease(&m_pLightSlateGrayBrush);
    SafeRelease(&m_pCornflowerBlueBrush);
}

void DemoApp::RunMessageLoop()
{
    MSG msg;

    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
}

HRESULT DemoApp::OnRender()
{
    HRESULT hr = S_OK;

    hr = CreateDeviceResources();

    if (SUCCEEDED(hr))
    {
        m_pRenderTarget->BeginDraw();
        m_pRenderTarget->SetTransform(D2D1::Matrix3x2F::Identity());
        m_pRenderTarget->Clear(D2D1::ColorF(D2D1::ColorF::White));

        D2D1_SIZE_F rtSize = m_pRenderTarget->GetSize();

        int width = static_cast<int>(rtSize.width);
        int height = static_cast<int>(rtSize.height);

        for (int x = 0; x < width; x += 10)
        {
            m_pRenderTarget->DrawLine(
                    D2D1::Point2F(static_cast<FLOAT>(x), 0.0f),
                    D2D1::Point2F(static_cast<FLOAT>(x), rtSize.height),
                    m_pLightSlateGrayBrush, 0.5f
                    );
        }

        for (int y = 0; y < height; y += 10)
        {
            m_pRenderTarget->DrawLine(
                    D2D1::Point2F(0.0f, static_cast<FLOAT>(y)),
                    D2D1::Point2F(rtSize.width, static_cast<FLOAT>(y)),
                    m_pLightSlateGrayBrush, 0.5f
                    );
        }

        D2D1_RECT_F rectangle1 = D2D1::RectF(
                rtSize.width / 2 - 50.f, rtSize.height / 2 - 50.f,
                rtSize.width / 2 + 50.f, rtSize.height / 2 + 50.f
                );
        D2D1_RECT_F rectangle2 = D2D1::RectF(
                rtSize.width / 2 - 100.f, rtSize.height / 2 - 100.f,
                rtSize.width / 2 + 100.f, rtSize.height / 2 + 100.f
                );

        m_pRenderTarget->FillRectangle(&rectangle1, m_pLightSlateGrayBrush);
        m_pRenderTarget->DrawRectangle(&rectangle2, m_pCornflowerBlueBrush);

        hr = m_pRenderTarget->EndDraw();
    }

    if (hr == D2DERR_RECREATE_TARGET)
    {
        hr = S_OK;
        DiscardDeviceResources();
    }

    return hr;
}

void DemoApp::OnResize(UINT width, UINT height)
{
    if (m_pRenderTarget)
    {
        m_pRenderTarget->Resize(D2D1::SizeU(width, height));
    }
}

LRESULT CALLBACK DemoApp::WndProc(HWND hwnd, UINT message, WPARAM wparam, LPARAM IParam)
{
    LRESULT result = 0;

    if (message == WM_CREATE)
    {
        LPCREATESTRUCT pcs = (LPCREATESTRUCT)IParam;
        StaticObject = (DemoApp*)pcs->lpCreateParams;

        result = 1;
    }
    else
    {
        bool wasHandled = false;

        if (StaticObject)
        {
            switch (message)
            {
                case WM_SIZE:
                {
                    UINT width = LOWORD(IParam);
                    UINT height = HIWORD(IParam);
                    StaticObject->OnResize(width, height);
                }
                    result = 0;
                    wasHandled = true;
                    break;

                case WM_DISPLAYCHANGE:
                {
                    InvalidateRect(hwnd, NULL, FALSE);
                }
                    result = 0;
                    wasHandled = true;
                    break;

                case WM_PAINT:
                {
                    StaticObject->OnRender();
                    ValidateRect(hwnd, NULL);
                }
                    result = 0;
                    wasHandled = true;
                    break;

                case WM_DESTROY:
                {
                    PostQuitMessage(0);
                }
                    result = 0;
                    wasHandled = true;
                    break;
            }
        }

        if (!wasHandled)
        {
            result = DefWindowProc(hwnd, message, wparam, IParam);
        }
    }

    return result;
}