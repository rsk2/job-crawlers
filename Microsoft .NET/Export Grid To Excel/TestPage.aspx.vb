Imports Microsoft.Office.Interop.Excel
Imports System.Drawing
Imports System.IO

Public Class TestPage
    Inherits System.Web.UI.Page

    Protected Sub Page_Load(ByVal sender As Object, ByVal e As System.EventArgs) Handles Me.Load

    End Sub

    Private Sub cmdExport_Click(sender As Object, e As System.EventArgs) Handles cmdExport.Click
	'You need an Export folder inside your project
        Dim directoryName As String = Server.MapPath("~/Export/")
        Dim localExcelPath As String = directoryName & lblTitle.InnerText & ".xlsx"
        'Just in case there is a file existing with same name
        localExcelPath = CheckAndRenameIfFileExists(localExcelPath)

        Dim excel = New Application()
        excel.Visible = True
        Dim wb As Workbook = excel.Workbooks.Add(XlWBATemplate.xlWBATWorksheet)
        Dim sh As Worksheet = wb.Sheets.Add()
        sh.Name = "Scorecard"
        Dim tb As New Table()
        Dim rowCount As Integer = 1
        AddGridToWorksheet(gvTest1, tb, sh, rowCount)
        AddGridToWorksheet(gvTest2, tb, sh, rowCount)
        sh.Columns.AutoFit()
        wb.SaveAs(localExcelPath)
        wb.Close(True)
        excel.Quit()
        Response.Clear()
        Response.Charset = ""
        Response.Buffer = True
        Response.ContentType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        Response.AddHeader("content-disposition", "attachment;filename=" & lblTitle.InnerText & ".xlsx")
        Response.TransmitFile((localExcelPath))
        Response.End()
    End Sub

    Private Function GetExcelColumnName(columnNumber As Integer) As String
        Dim dividend As Integer = columnNumber
        Dim columnName As String = String.Empty
        Dim modulo As Integer

        While dividend > 0
            modulo = (dividend - 1) Mod 26
            columnName = Convert.ToChar(65 + modulo).ToString() & columnName
            dividend = CInt((dividend - modulo) / 26)
        End While

        Return columnName
    End Function

    Private Function CheckAndRenameIfFileExists(fullPath As String) As String
        Dim count As Integer = 0
        Dim fileNameOnly As String = Path.GetFileNameWithoutExtension(fullPath)
        Dim extension As String = Path.GetExtension(fullPath)
        Dim directory As String = Path.GetDirectoryName(fullPath)
        Dim newFullPath As String = fullPath
        Dim tempFileName As String
        While (File.Exists(newFullPath))
            count += 1
            tempFileName = String.Format("{0}({1})", fileNameOnly, count)
            newFullPath = Path.Combine(directory, tempFileName + extension)
        End While
        Return newFullPath
    End Function

    Public Sub AddGridToWorksheet(gvCtrl As GridView, tb As Table, sh As Worksheet, ByRef rowCount As Integer)
        If gvCtrl.Visible = True Then
            Dim j As Integer = 1
            For Each cell As TableCell In gvCtrl.HeaderRow.Cells
                If cell.Text <> "&nbsp;" Then
                    sh.Cells(rowCount, GetExcelColumnName(j)).Value = cell.Text
                    j = j + 1
                End If
            Next
	    rowCount += 1

            Dim data, num, den, percent, count, amount, mintCalcColumnNumber, rowHeight As String
            Dim isPercentage, isCurrency As Boolean
            Dim i, k As Integer
            Dim lnkYTDCtrl As LinkButton

            For Each row As GridViewRow In gvCtrl.Rows
                sh.Cells(rowCount, GetExcelColumnName(1)).Value = row.Cells(0).Text
                sh.Cells(rowCount, GetExcelColumnName(2)).Value = row.Cells(1).Text
		'Sets wrap text as true and makes text center for columns from 3 to 14. You would want to readjust this based on size of your grid
                sh.Range(sh.Cells(rowCount, GetExcelColumnName(3)), sh.Cells(rowCount, GetExcelColumnName(14))).WrapText = True
                sh.Range(sh.Cells(rowCount, GetExcelColumnName(3)), sh.Cells(rowCount, GetExcelColumnName(14))).HorizontalAlignment = Microsoft.Office.Interop.Excel.Constants.xlCenter

                Dim period As Integer = Utilities.CIntN(row.Cells(2).Text)
                If period = 3 Then
                    For i = 3 To 12 Step 3
                        sh.Range(sh.Cells(rowCount, GetExcelColumnName(i)), sh.Cells(rowCount, GetExcelColumnName(i + 2))).Merge()
                    Next
                    'The merged cells heights are not adjusted properly to fit the text inspite of the wrap text being true and so below two lines are necessary
                    rowHeight = Utilities.CIntN(sh.Range(sh.Cells(rowCount, GetExcelColumnName(3)), sh.Cells(rowCount, GetExcelColumnName(14))).RowHeight)
                    sh.Range(sh.Cells(rowCount, GetExcelColumnName(3)), sh.Cells(rowCount, GetExcelColumnName(14))).RowHeight = rowHeight * 2
                End If

                'Set the bg color for each cell in row - no easy way to copy the values from the CSS. Only required if you have colors on grid
                For i = mintFirstClassColumn To (mintFirstCalcColumn - 1)
                    If row.Cells(i).Text = "GoalNotMet" Then
                        sh.Range(sh.Cells(rowCount, GetExcelColumnName(i)), sh.Cells(rowCount, GetExcelColumnName(i))).Interior.Color = Color.Pink
                    ElseIf row.Cells(i).Text = "GoalMet" Then
                        sh.Range(sh.Cells(rowCount, GetExcelColumnName(i)), sh.Cells(rowCount, GetExcelColumnName(i))).Interior.Color = Color.LightGreen
                    ElseIf row.Cells(i).Text = "GoalClose" Then
                        sh.Range(sh.Cells(rowCount, GetExcelColumnName(i)), sh.Cells(rowCount, GetExcelColumnName(i))).Interior.Color = Color.Yellow
                    End If
                Next

                              rowCount += 1
            Next
            'add a blank row after each grid
            rowCount += 1
        End If
    End Sub

  
End Class
