
namespace restAPI
{
    partial class MainForm
    {
        /// <summary>
        /// 필수 디자이너 변수입니다.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 사용 중인 모든 리소스를 정리합니다.
        /// </summary>
        /// <param name="disposing">관리되는 리소스를 삭제해야 하면 true이고, 그렇지 않으면 false입니다.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 디자이너에서 생성한 코드

        /// <summary>
        /// 디자이너 지원에 필요한 메서드입니다. 
        /// 이 메서드의 내용을 코드 편집기로 수정하지 마세요.
        /// </summary>
        private void InitializeComponent()
        {
            this.ServerStart_btn = new System.Windows.Forms.Button();
            this.Request_richTBox = new System.Windows.Forms.RichTextBox();
            this.SuspendLayout();
            // 
            // ServerStart_btn
            // 
            this.ServerStart_btn.Location = new System.Drawing.Point(12, 12);
            this.ServerStart_btn.Name = "ServerStart_btn";
            this.ServerStart_btn.Size = new System.Drawing.Size(137, 50);
            this.ServerStart_btn.TabIndex = 0;
            this.ServerStart_btn.Text = "서버 구동";
            this.ServerStart_btn.UseVisualStyleBackColor = true;
            this.ServerStart_btn.Click += new System.EventHandler(this.serverStartBtnOnClick);
            // 
            // Request_richTBox
            // 
            this.Request_richTBox.Location = new System.Drawing.Point(12, 82);
            this.Request_richTBox.Name = "Request_richTBox";
            this.Request_richTBox.Size = new System.Drawing.Size(658, 409);
            this.Request_richTBox.TabIndex = 1;
            this.Request_richTBox.Text = "";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 17F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(682, 503);
            this.Controls.Add(this.Request_richTBox);
            this.Controls.Add(this.ServerStart_btn);
            this.Font = new System.Drawing.Font("굴림", 10F);
            this.Name = "MainForm";
            this.Text = "버서";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button ServerStart_btn;
        private System.Windows.Forms.RichTextBox Request_richTBox;
    }
}

