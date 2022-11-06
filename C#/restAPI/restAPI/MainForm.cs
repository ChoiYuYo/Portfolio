using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace restAPI
{
    public partial class MainForm : Form
    {
        HttpListener httpListener;

        public MainForm()
        {
            InitializeComponent();
        }

        private void serverStartBtnOnClick(object sender, EventArgs e)
        {
            if (httpListener == null)
            {
                httpListener = new HttpListener();
                httpListener.Prefixes.Add(string.Format("http://+:8080/"));
                serverStart();
            }
        }
        
        private void serverStart()
        {
            if (!httpListener.IsListening)
            {
                httpListener.Start();
                Request_richTBox.Text = "Server is Started";

                Task.Factory.StartNew(() =>
                {
                    while (httpListener != null)
                    {
                        HttpListenerContext context = this.httpListener.GetContext();

                        string rawurl = context.Request.RawUrl;
                        string httpmethod = context.Request.HttpMethod;

                        string result = "";

                        result += string.Format("httpmethod = {0}\r\n", httpmethod);
                        result += string.Format("rawurl = {0}\r\n", rawurl);

                        if (Request_richTBox.InvokeRequired)
                            Request_richTBox.Invoke(new MethodInvoker(delegate { Request_richTBox.Text = result; }));
                        else
                            Request_richTBox.Text = result;

                        context.Response.Close();
                    }
                });
            }
        }
    }
}
