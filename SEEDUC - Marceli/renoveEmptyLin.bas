Attribute VB_Name = "Módulo4"
Sub ExcluirLinhasVazias()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    
    ' Defina a planilha na qual você deseja excluir as linhas vazias
    Set ws = ThisWorkbook.Sheets("Planilha1") ' Altere "Planilha1" para o nome da sua planilha
    
    ' Encontre a última linha com dados na coluna A
    lastRow = ws.Cells(ws.Rows.Count, "A").End(xlUp).Row
    
    ' Percorra as linhas da planilha da última linha até a primeira
    For i = lastRow To 1 Step -1
        ' Verifique se a linha está vazia
        If WorksheetFunction.CountA(ws.Rows(i)) = 0 Then
            ' Se a linha estiver vazia, exclua-a
            ws.Rows(i).Delete
        End If
    Next i
End Sub



