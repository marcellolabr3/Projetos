Attribute VB_Name = "Módulo5"
Sub ExcluirColunasVazias()

    Dim ws As Worksheet
    Dim i As Long
    
    ' Defina a planilha na qual você deseja excluir as colunas
    Set ws = ThisWorkbook.Sheets("Planilha1") ' Altere "Planilha1" para o nome da sua planilha
    
    ' Percorre todas as colunas da planilha
    For i = ws.Cells(1, ws.Columns.Count).End(xlToLeft).Column To 1 Step -1
        ' Verifica se o nome da coluna começa com "Coluna"
        If Left(ws.Cells(1, i).Value, 6) = "Coluna" Then
            ' Exclui a coluna
            ws.Columns(i).Delete
        End If
    Next i
End Sub

