import streamlit as st
from datetime import datetime

def show_success(message, details=None, icon="✅"):
    """
    Exibe uma mensagem de sucesso padronizada em todo o sistema
    """
    # Toast notification
    st.toast(f"{icon} {message}", icon=icon)
    
    # Mensagem principal
    if details:
        st.success(f"""
        ### {icon} {message}
        
        {details}
        """)
    else:
        st.success(f"{icon} {message}")

def show_error(message, details=None, icon="❌"):
    """
    Exibe uma mensagem de erro padronizada em todo o sistema
    """
    st.toast(f"{icon} {message}", icon=icon)
    
    if details:
        st.error(f"""
        ### {icon} {message}
        
        {details}
        """)
    else:
        st.error(f"{icon} {message}")

def show_warning(message, details=None, icon="⚠️"):
    """
    Exibe um aviso padronizado em todo o sistema
    """
    st.toast(f"{icon} {message}", icon=icon)
    
    if details:
        st.warning(f"""
        ### {icon} {message}
        
        {details}
        """)
    else:
        st.warning(f"{icon} {message}")

def show_info(message, details=None, icon="ℹ️"):
    """
    Exibe uma informação padronizada em todo o sistema
    """
    st.toast(f"{icon} {message}", icon=icon)
    
    if details:
        st.info(f"""
        ### {icon} {message}
        
        {details}
        """)
    else:
        st.info(f"{icon} {message}")

def show_batch_result(success_count, error_count, total, entity="registros", details=None):
    """
    Exibe resultado de operações em lote
    """
    if success_count > 0:
        st.toast(f"✅ {success_count} {entity} processados com sucesso!", icon="🎉")
    
    if success_count == total:
        st.success(f"""
        ### 🎉 Operação em Lote Concluída!
        
        | | |
        |---|---|
        | **Total processado** | {total} |
        | **✅ Sucessos** | {success_count} |
        | **❌ Falhas** | {error_count} |
        | **Taxa de sucesso** | {(success_count/total*100):.1f}% |
        
        {details if details else ""}
        """)
    else:
        st.warning(f"""
        ### ⚠️ Operação em Lote Parcialmente Concluída
        
        | | |
        |---|---|
        | **Total processado** | {total} |
        | **✅ Sucessos** | {success_count} |
        | **❌ Falhas** | {error_count} |
        | **Taxa de sucesso** | {(success_count/total*100):.1f}% |
        
        {details if details else ""}
        """)

def show_operation_result(operation, success, entity_name, details=None):
    """
    Exibe resultado de uma operação individual
    """
    if success:
        st.toast(f"✅ {operation} realizado com sucesso!", icon="✨")
        st.success(f"""
        ### ✅ {operation} Realizado com Sucesso!
        
        **{entity_name}** foi {operation.lower()} com sucesso.
        {details if details else ""}
        """)
    else:
        st.toast(f"❌ Erro ao realizar {operation}", icon="⚠️")
        st.error(f"""
        ### ❌ Erro ao Realizar {operation}
        
        Não foi possível {operation.lower()} **{entity_name}**.
        {details if details else "Tente novamente ou contate o suporte."}
        """)